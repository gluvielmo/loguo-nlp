from pathlib import Path
import pandas as pd
from pipeline.schemas import JournalEntry

def load_entries(csv_path: str | Path, source: str = "") -> list[JournalEntry]:
    df = pd.read_csv(csv_path)
    entries = []

    for i, row in df.iterrows():
        raw = row.get("text")

        if pd.isna(raw):
            continue

        text = str(raw).strip()

        if not text:
            continue

        entry = JournalEntry(
            id=f"{source}_{i:04d}",
            date=pd.to_datetime(row["date"]).date(),
            text=text,
            source=source,
            metadata={
                "title": str(row.get("title", "") or ""),
                "url": str(row.get("url", "") or ""),
            }
        )

        entries.append(entry)

    return entries