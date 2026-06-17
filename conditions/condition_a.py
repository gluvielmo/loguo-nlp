import json
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

from pipeline.costs import GENERATION_MODEL, estimate_cost
from pipeline.data.loader import load_entries
from pipeline.schemas import ConditionArtifacts, Report, RunMetrics, TemporalAnalysis, Theme

load_dotenv()

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


_SYSTEM_PROMPT = (
    "You are an expert in longitudinal analysis of personal writing. "
    "Write exclusively in second person (\"you wrote...\", \"your entries...\", \"your writing...\"). "
    "Your role is to describe and analyze patterns in the corpus — not to advise. "
    "Never use phrases like \"you should\", \"you might consider\", \"it would be helpful to\", "
    "\"this suggests you would benefit from\", or any construction that implies what the writer "
    "should do, even when softened or embedded in an otherwise descriptive sentence. "
    "If a finding has an obvious actionable implication, state the finding only — not the implied action. "
    "Hedge all interpretive claims: use language like \"this may suggest...\", "
    "\"this could reflect...\", or \"one possible reading is...\". "
    "Psychological interpretation must be explicitly marked as speculative."
)


def run(csv_path: str, source: str) -> ConditionArtifacts:
    total_start = time.time()

    entries = load_entries(csv_path, source=source)
    entries = entries[:500]

    entry_lines = "\n\n".join(
        f"[{e.date}] {e.text[:400]}"
        for e in entries
    )

    prompt = f"""Analyze this longitudinal journal corpus spanning multiple years.

Below are {len(entries)} journal entries in chronological order:

{entry_lines}

Respond with a JSON object with exactly these keys:

"main_themes"
A list of objects, each with:
  "name": a short label for the theme
  "description": 1–2 sentences describing what this theme covers

"corpus_overview"
A single prose paragraph (second person) covering:
- Total volume and time span
- Dominant theme(s) by approximate proportion of entries
- Notable minority or marginal themes — not just the most frequent
- Overall compositional character

"temporal_arc"
A list of objects covering the full time span in 3–5 chronological periods. Each object must have:
  "period": a label for this period (e.g. "2009–2012", "early", "2015–2018")
  "theme_composition": 1–2 sentences on which themes dominated this period and how they shifted relative to adjacent periods
  "linguistic_register": 1–2 sentences on how the tone, style, or emotional register of the writing shifted in this period (no LFE metrics are available for this condition — describe qualitatively from the entry content)

"synthesis"
A single closing paragraph connecting the dominant themes to the writing style patterns over time.
Mark any psychological interpretation as speculative. Do not offer advice or recommendations.

"limitations"
A list of 2–3 strings identifying genuine limitations of this analysis.
"""

    client = _get_client()

    llm_start = time.time()
    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    )
    llm_secs = time.time() - llm_start

    data = json.loads(response.choices[0].message.content)
    usage = response.usage

    report = Report(
        condition_name="A: LLM Baseline",
        corpus_size=len(entries),
        date_range=(min(e.date for e in entries), max(e.date for e in entries)),
        generated_at=datetime.utcnow(),
        main_themes=[
            Theme(name=t["name"], description=t["description"], entry_ids=[])
            for t in data.get("main_themes", [])
        ],
        subthemes=[],
        temporal_analysis=TemporalAnalysis(
            corpus_overview=str(data.get("corpus_overview", "")),
            temporal_arc=data.get("temporal_arc", []),
            synthesis=str(data.get("synthesis", "")),
        ),
        linguistic_patterns={},
        representative_evidence=[],
        limitations=data.get("limitations", []),
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
        condition="A: LLM Baseline",
        corpus_id=source,
        run_timestamp=datetime.utcnow(),
        report=report,
        topics_or_clusters=[],
        lfe_per_entry=[],
        lfe_aggregated={},
        metrics=metrics,
    )
