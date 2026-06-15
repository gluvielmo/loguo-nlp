import time
from datetime import datetime
from pathlib import Path
from statistics import mean

from pipeline.costs import GENERATION_MODEL, EMBEDDING_MODEL, estimate_cost
from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed
from pipeline.lfe.extractor import extract_batch
from pipeline.schemas import ConditionArtifacts, RunMetrics
from pipeline.clustering.hierarchical import run as cluster_run
from pipeline.labeling.keyword_labeler import label_all as kw_label_all
from pipeline.synthesis.report_generator import generate


def run(csv_path: str, source: str, n_clusters: int = 20) -> ConditionArtifacts:
    total_start = time.time()

    entries = load_entries(csv_path, source)
    entries = entries[:500]

    # embed — tokens=0 means cache hit (no API call)
    t0 = time.time()
    vecs, embed_tokens = embed(entries, cache_dir=Path("outputs/embeddings_cache"))
    embed_secs = time.time() - t0

    # clustering: local agglomerative fit
    t0 = time.time()
    clusters = cluster_run(entries, vecs, n_clusters)
    cluster_secs = time.time() - t0

    # keyword labeling: pure TF-IDF, no LLM calls
    t0 = time.time()
    entries_by_id = {e.id: e for e in entries}
    clusters = kw_label_all(clusters, entries_by_id)
    kw_secs = time.time() - t0

    # LFE: local spaCy processing
    t0 = time.time()
    lfe_list = extract_batch(entries)
    lfe_secs = time.time() - t0

    # generate report: one tracked LLM call
    t0 = time.time()
    report, gen_in, gen_out = generate("Hierarchical Clustering + Keyword Labels", entries, clusters, lfe_list)
    gen_secs = time.time() - t0

    total_secs = time.time() - total_start

    llm_secs = gen_secs + (embed_secs if embed_tokens > 0 else 0.0)
    preprocessing_secs = cluster_secs + kw_secs + lfe_secs + (0.0 if embed_tokens > 0 else embed_secs)

    metrics = RunMetrics(
        total_seconds=round(total_secs, 2),
        preprocessing_seconds=round(preprocessing_secs, 2),
        llm_seconds=round(llm_secs, 2),
        llm_calls=1,  # only generate; keyword labeling has no LLM calls
        input_tokens=gen_in,
        output_tokens=gen_out,
        generation_model=GENERATION_MODEL,
        embedding_tokens=embed_tokens,
        embedding_entries=len(entries),
        embedding_model=EMBEDDING_MODEL,
        estimated_cost_usd=estimate_cost(
            embedding_tokens=embed_tokens,
            input_tokens=gen_in,
            output_tokens=gen_out,
        ),
    )

    return ConditionArtifacts(
        condition="Hierarchical Clustering + Keyword Labels",
        corpus_id=source,
        run_timestamp=datetime.utcnow(),
        report=report,
        topics_or_clusters=[c.model_dump() for c in clusters],
        lfe_per_entry=lfe_list,
        lfe_aggregated={
            "avg_word_count": mean(f.word_count for f in lfe_list),
            "avg_negation_count": mean(f.negation_count for f in lfe_list),
        },
        metrics=metrics,
    )
