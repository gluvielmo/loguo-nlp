import json

from pipeline.embeddings.embedder import _get_client
from pipeline.schemas import Cluster, JournalEntry


def label_cluster(cluster: Cluster, entries_by_id: dict[str, JournalEntry]) -> Cluster:
    texts = [entries_by_id[eid].text for eid in cluster.representative_entry_ids]

    formatted_texts = "\n---\n".join(
        f"Entry {i+1}:\n{text}" for i, text in enumerate(texts)
    )

    prompt = f"""You are analyzing journal entries grouped into a thematic cluster.

    Here are {len(texts)} representative entries from this cluster:

    ---
    {formatted_texts}
    ---

    Based on these entries, identify the recurring psychological or emotional theme.

    Respond with a JSON object with exactly these keys:
    - "label": a 3-5 word theme name (e.g. "Grief and loss", "Work pressure and burnout")
    - "description": one paragraph describing the pattern you observe across these entries
    - "subthemes": a list of 3-5 strings naming more specific patterns within this theme
    """

    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert in psychological analysis of personal writing."},
            {"role": "user", "content": prompt}
        ]
    )

    data = json.loads(response.choices[0].message.content)

    return cluster.model_copy(update={
        "label": data["label"],
        "description": data["description"],
        "subthemes": data["subthemes"],
        "labeling_method": "llm"
    })

def label_all(clusters: list[Cluster], entries_by_id: dict[str, JournalEntry]) -> list[Cluster]:
    return [label_cluster(c, entries_by_id) for c in clusters]