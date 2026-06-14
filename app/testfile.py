from pathlib import Path
from pipeline.clustering.hierarchical import run as cluster_run
from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed

entries = load_entries("data/dooce_2009_2023.csv", source="dooce")
vecs = embed(entries, cache_dir=Path("outputs/embeddings_cache"))

clusters = cluster_run(entries, vecs, n_clusters=10)
print(len(clusters))
print(clusters[0])
