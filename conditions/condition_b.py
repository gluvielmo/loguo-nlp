import time
from datetime import datetime
from statistics import mean

from pipeline.costs import GENERATION_MODEL, estimate_cost
from pipeline.data.loader import load_entries
from pipeline.lfe.extractor import extract_batch
from pipeline.schemas import ConditionArtifacts, RunMetrics
from pipeline.synthesis.report_generator import generate


def run(csv_path: str, source: str) -> ConditionArtifacts:
    total_start = time.time()

    entries = load_entries(csv_path, source)
    entries = entries[:500]

    # LFE only — no clustering, no embeddings
    t0 = time.time()
    lfe_list = extract_batch(entries)
    lfe_secs = time.time() - t0

    t0 = time.time()
    report, gen_in, gen_out = generate("B: LFE Only", entries, [], lfe_list)
    gen_secs = time.time() - t0

    total_secs = time.time() - total_start

    metrics = RunMetrics(
        total_seconds=round(total_secs, 2),
        preprocessing_seconds=round(lfe_secs, 2),
        llm_seconds=round(gen_secs, 2),
        llm_calls=1,
        input_tokens=gen_in,
        output_tokens=gen_out,
        generation_model=GENERATION_MODEL,
        embedding_tokens=0,
        embedding_entries=0,
        embedding_model="",
        estimated_cost_usd=estimate_cost(
            embedding_tokens=0,
            input_tokens=gen_in,
            output_tokens=gen_out,
        ),
    )

    return ConditionArtifacts(
        condition="B: LFE Only",
        corpus_id=source,
        run_timestamp=datetime.utcnow(),
        report=report,
        topics_or_clusters=[],
        lfe_per_entry=lfe_list,
        lfe_aggregated={
            "avg_word_count": mean(f.word_count for f in lfe_list),
            "avg_negation_count": mean(f.negation_count for f in lfe_list),
        },
        metrics=metrics,
    )
