from pathlib import Path
from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed

entries = load_entries("data/dooce_2009_2023.csv", source="dooce")

vecs = embed(entries[:5], cache_dir=Path("outputs/embeddings_cache"))

print(vecs.shape)