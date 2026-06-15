from datetime import datetime
from pathlib import Path
import time
from statistics import mean

from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed
from pipeline.lfe.extractor import extract_batch
from pipeline.schemas import ConditionArtifacts
from pipeline.clustering.hierarchical import run as cluster_run
from pipeline.labeling.llm_labeler import label_all as llm_label_all
from pipeline.synthesis.report_generator import generate


def run(csv_path: str, source: str, n_clusters: int = 20) -> ConditionArtifacts:
    start = time.time()

    entries = load_entries(csv_path, source)
    entries = entries[:500]

    vecs = embed(entries, cache_dir=Path("outputs/embeddings_cache"))

    clusters = cluster_run(entries, vecs, n_clusters)

    entries_by_id = {e.id: e for e in entries}
    clusters = llm_label_all(clusters, entries_by_id)

    lfe_list = extract_batch(entries)

    report = generate("Hierarchical Clustering + LLM Labels", entries, clusters, lfe_list)

    runtime = time.time() - start

    return ConditionArtifacts(
        condition="Hierarchical Clustering + LLM Labels",
        corpus_id=source,
        run_timestamp=datetime.utcnow(),
        report=report,
        topics_or_clusters=[c.model_dump() for c in clusters],
        lfe_per_entry=lfe_list,
        lfe_aggregated={
            "avg_word_count": mean(f.word_count for f in lfe_list),
            "avg_negation_count": mean(f.negation_count for f in lfe_list),
        },
        runtime_seconds=runtime,
    )
