from datetime import datetime
from pathlib import Path
import time
from statistics import mean

from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed
from pipeline.lfe.extractor import extract_batch
from pipeline.schemas import ConditionArtifacts
from pipeline.topic_modeling.bertopic_runner import run as bertopic_run, assignments_to_clusters
from pipeline.synthesis.report_generator import generate


def run(csv_path: str, source: str) -> ConditionArtifacts:
    start = time.time()

    entries = load_entries(csv_path, source)
    entries = entries[:500]

    vecs = embed(entries, cache_dir=Path("outputs/embeddings_cache"))

    assignments = bertopic_run(entries, vecs)

    clusters = assignments_to_clusters(assignments)

    lfe_list = extract_batch(entries)

    report = generate("condition2_bertopic", entries, clusters, lfe_list)

    runtime = time.time() - start

    return ConditionArtifacts(
        condition="condition2",
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
