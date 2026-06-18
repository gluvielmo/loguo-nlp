import json
import re
from collections import Counter

from pipeline.embeddings.embedder import _get_client
from pipeline.schemas import Cluster, JournalEntry

_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "i", "you", "he", "she",
    "it", "we", "they", "me", "him", "her", "us", "them", "my", "your",
    "his", "its", "our", "their", "this", "that", "these", "those",
    "not", "no", "so", "as", "if", "when", "than", "then", "just",
    "about", "up", "out", "what", "which", "who", "there", "all", "one",
    "got", "get", "like", "know", "think", "going", "said", "says", "say",
}


def _tokenize(text: str) -> list[str]:
    return [w for w in re.findall(r'\b[a-z]{3,}\b', text.lower()) if w not in _STOP_WORDS]


def _distinctive_words(
    cluster: Cluster,
    entries_by_id: dict[str, JournalEntry],
    corpus_freq: Counter,
    corpus_size: int,
    n: int = 10,
) -> list[str]:
    cluster_words = [
        word
        for eid in cluster.entry_ids
        if eid in entries_by_id
        for word in _tokenize(entries_by_id[eid].text)
    ]
    cluster_size = len(cluster_words)
    if cluster_size == 0:
        return []

    cluster_freq = Counter(cluster_words)
    scores = {
        word: (count / cluster_size) / (corpus_freq[word] / corpus_size)
        for word, count in cluster_freq.items()
        if corpus_freq[word] > 0
    }
    return [w for w, _ in sorted(scores.items(), key=lambda x: -x[1])[:n]]


def label_all(
    clusters: list[Cluster],
    entries_by_id: dict[str, JournalEntry],
) -> tuple[list[Cluster], int, int]:
    corpus_words = [word for entry in entries_by_id.values() for word in _tokenize(entry.text)]
    corpus_freq = Counter(corpus_words)
    corpus_size = len(corpus_words)

    cluster_blocks = []
    for i, cluster in enumerate(clusters):
        distinctive = _distinctive_words(cluster, entries_by_id, corpus_freq, corpus_size)
        texts = [entries_by_id[eid].text for eid in cluster.representative_entry_ids if eid in entries_by_id]
        formatted = "\n---\n".join(f"Entry {j+1}:\n{text}" for j, text in enumerate(texts))
        cluster_blocks.append(
            f"Cluster {i + 1}:\n"
            f"Distinctive words: {', '.join(distinctive)}\n"
            f"Representative entries:\n{formatted}"
        )

    all_blocks = "\n\n===\n\n".join(cluster_blocks)

    prompt = f"""You are analyzing journal entries grouped into thematic clusters.

For each cluster, identify the specific recurring topic or subject matter.

{all_blocks}

Respond with a JSON object with key "clusters" — a list with one object per cluster in the same order, each with:
- "label": a 3-5 word specific topic name. Be concrete and grounded in what the entries actually discuss (e.g. "Nursery decoration project", "Life with pets", "Running injury recovery"). Avoid abstract psychological language — not "Personal Growth", "Self-Discovery", or "Transition and Reflection".
- "description": one paragraph describing the specific recurring pattern across these entries
- "subthemes": a list of 3-5 strings naming more specific patterns within this topic
"""

    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert at identifying specific topics and subjects in personal writing."},
            {"role": "user", "content": prompt},
        ],
    )

    data = json.loads(response.choices[0].message.content)
    usage = response.usage

    labeled = [
        cluster.model_copy(update={
            "label": cluster_data["label"],
            "description": cluster_data["description"],
            "subthemes": cluster_data["subthemes"],
            "labeling_method": "llm",
        })
        for cluster, cluster_data in zip(clusters, data["clusters"])
    ]

    return labeled, usage.prompt_tokens, usage.completion_tokens
