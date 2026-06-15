import hashlib
from pathlib import Path
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

from pipeline.schemas import JournalEntry

load_dotenv()

_client = None

def _get_client():
    global _client

    if _client is None:
        _client = OpenAI()

    return _client

def _cache_key(entries: list[JournalEntry]) -> str:
    raw = "".join(e.id for e in entries)

    return hashlib.md5(raw.encode()).hexdigest()

def embed(entries: list[JournalEntry], cache_dir: Path, cache: bool = True) -> tuple[np.ndarray, int]:
    key = _cache_key(entries)

    cache_path = cache_dir / f"{key}.npy"

    if cache and cache_path.exists():
        return np.load(cache_path), 0

    client = _get_client()

    texts = [e.text for e in entries]
    all_embeddings = []
    total_tokens = 0

    for i in range(0, len(texts), 100):
        batch = texts[i:i+100]
        response = client.embeddings.create(input=batch, model="text-embedding-3-small")
        for item in response.data:
            all_embeddings.append(item.embedding)
        total_tokens += response.usage.total_tokens

    result = np.array(all_embeddings)

    if cache:
        cache_dir.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, result)

    return result, total_tokens