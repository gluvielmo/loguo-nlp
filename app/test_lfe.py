from pipeline.data.loader import load_entries
from pipeline.lfe.extractor import extract

entries = load_entries("data/dooce_2009_2023.csv", source="dooce")

from pipeline.lfe.extractor import extract_batch
results = extract_batch(entries[:3])
for r in results:
	print(r)