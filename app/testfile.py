from pathlib import Path
from pipeline.data.loader import load_entries
from pipeline.embeddings.embedder import embed
from pipeline.topic_modeling.bertopic_runner import run

entries = load_entries("data/dooce_2009_2023.csv", source="dooce")
vecs = embed(entries, cache_dir=Path("outputs/embeddings_cache"))
assignments = run(entries, vecs)

print(len(assignments))
print(assignments[0])
print(assignments[100])
