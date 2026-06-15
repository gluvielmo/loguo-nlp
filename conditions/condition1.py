import json
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from pipeline.costs import GENERATION_MODEL, estimate_cost
from pipeline.data.loader import load_entries
from pipeline.schemas import ConditionArtifacts, Report, RunMetrics, Theme

load_dotenv()

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def run(csv_path: str, source: str) -> ConditionArtifacts:
    total_start = time.time()

    entries = load_entries(csv_path, source=source)
    entries = entries[:500]

    entry_lines = "\n\n".join(
        f"[{e.date}] {e.text[:400]}"
        for e in entries
    )

    prompt = f"""You are analyzing a longitudinal journal corpus spanning multiple years.

Below are {len(entries)} journal entries in chronological order:

{entry_lines}

Based on these entries, produce a comprehensive longitudinal analysis.

Respond with a JSON object with exactly these keys:
- "main_themes": list of objects with "name" (string) and "description" (string)
- "temporal_evolution": dict mapping period labels to descriptions of how themes shifted (e.g. {{"2009-2012": "...", "2013-2017": "...", "2018-2023": "..."}})
- "surprising_patterns": list of 3-5 strings describing unexpected findings
- "reflection_questions": list of 5 questions the journaler could reflect on
- "limitations": list of 2-3 strings describing limitations of this analysis
"""

    client = _get_client()

    llm_start = time.time()
    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert in longitudinal analysis of personal writing and psychological patterns."
            },
            {"role": "user", "content": prompt}
        ]
    )
    llm_secs = time.time() - llm_start

    data = json.loads(response.choices[0].message.content)
    usage = response.usage

    report = Report(
        condition_name="LLM Only Baseline",
        corpus_size=len(entries),
        date_range=(min(e.date for e in entries), max(e.date for e in entries)),
        generated_at=datetime.utcnow(),
        main_themes=[
            Theme(name=t["name"], description=t["description"], entry_ids=[])
            for t in data["main_themes"]
        ],
        subthemes=[],
        temporal_evolution=data["temporal_evolution"],
        linguistic_patterns={},
        representative_evidence=[],
        surprising_patterns=data["surprising_patterns"],
        reflection_questions=data["reflection_questions"],
        limitations=data["limitations"],
    )

    total_secs = time.time() - total_start

    metrics = RunMetrics(
        total_seconds=round(total_secs, 2),
        preprocessing_seconds=0.0,
        llm_seconds=round(llm_secs, 2),
        llm_calls=1,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        generation_model=GENERATION_MODEL,
        embedding_tokens=0,
        embedding_entries=0,
        embedding_model="",
        estimated_cost_usd=estimate_cost(
            embedding_tokens=0,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
        ),
    )

    return ConditionArtifacts(
        condition="LLM Only Baseline",
        corpus_id=source,
        run_timestamp=datetime.utcnow(),
        report=report,
        topics_or_clusters=[],
        lfe_per_entry=[],
        lfe_aggregated={},
        metrics=metrics,
    )
