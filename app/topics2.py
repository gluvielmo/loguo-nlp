import json
import numpy as np
import os

from supabase import create_client
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
MIN_ENTRIES  = 30
USER_ID      = "9419df97-5c20-4e29-acc8-980e25e6ffc6"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def build_models(n_docs: int) -> tuple[BERTopic, UMAP, HDBSCAN]:
    n_neighbors = min(10, n_docs // 3)

    umap_model = UMAP(
        n_neighbors  = n_neighbors,
        n_components = 5,
        min_dist     = 0.0,
        metric       = "cosine",
        random_state = 42,
    )
    hdbscan_model = HDBSCAN(
        min_cluster_size = 2,
        min_samples      = 1,
        metric           = "euclidean",
        prediction_data  = True,
    )

    vectorizer = CountVectorizer(
        stop_words = "english",
        min_df     = 2,
        ngram_range = (1, 2),
        token_pattern = r"(?u)\b[a-zA-Z]{3,}\b", #ballard's
    )

    topic_model = BERTopic(
        umap_model    = umap_model,
        hdbscan_model = hdbscan_model,
        vectorizer_model = vectorizer,
        nr_topics="auto",
        min_topic_size=2,
        verbose       = False,
    )
    return topic_model, umap_model, hdbscan_model


def run():
    rows = (
        supabase.from_("entries")
        .select("id, content, embedding")
        .eq("user_id", USER_ID)
        .limit(50)
        .execute()
        .data
    )

    n = len(rows)
    print(f"User {USER_ID} - {n} entries")

    if n < MIN_ENTRIES:
        print(f"Skipping: below {MIN_ENTRIES} entries")
        return

    docs       = [r["content"] for r in rows]
    embeddings = np.array(
        [json.loads(r["embedding"]) if isinstance(r["embedding"], str) else r["embedding"] for r in rows],
        dtype=np.float32
    )

    topic_model, _, _ = build_models(n)
    topics, probs     = topic_model.fit_transform(docs, embeddings)

    topic_info = topic_model.get_topic_info()
    n_topics   = len(topic_info[topic_info["Topic"] != -1])
    print(f"\nTopics found: {n_topics}  |  Outliers: {sum(t == -1 for t in topics)}")

    print("\n── Topic Summary ─────────────────────────────────────────────")
    print(topic_info[topic_info["Topic"] != -1][["Topic", "Count", "Name"]].to_string(index=False))

    # ── Visualize ─────────────────────────────────────────────────────────────

    umap_2d = UMAP(
        n_neighbors  = min(10, n // 3),
        n_components = 2,
        min_dist     = 0.1,
        metric       = "cosine",
        random_state = 42,
    )
    embeddings_2d = umap_2d.fit_transform(embeddings)

    topic_model.visualize_documents(
        docs,
        reduced_embeddings = embeddings_2d,
        hide_annotations   = False,
    ).show()


if __name__ == "__main__":
    run()