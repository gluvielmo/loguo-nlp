import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

from pipeline.schemas import Cluster, JournalEntry


def label_all(clusters: list[Cluster], entries_by_id: dict[str, JournalEntry]) -> list[Cluster]:
    cluster_docs = []

    for cluster in clusters:
        combined = " ".join(entries_by_id[eid].text for eid in cluster.entry_ids)
        cluster_docs.append(combined)
    
    custom_stop_words = [
        "like", "just", "going", "really", "know", "got", "get", "said",
        "thing", "things", "think", "thought", "want", "wanted", "need",
        "time", "day", "year", "people", "little", "way", "make", "ll",
        "ve", "didn", "wasn", "isn", "couldn", "wouldn", "don", "doesn",
    ]

    vectorizer = TfidfVectorizer(
        stop_words=list(ENGLISH_STOP_WORDS) + custom_stop_words,
        max_features=1000,
        ngram_range=(1, 2),
    )
    tfidf_matrix = vectorizer.fit_transform(cluster_docs)
    terms = vectorizer.get_feature_names_out()

    updated_clusters = []

    for i, cluster in enumerate(clusters):
        row = tfidf_matrix[i].toarray()[0]
        top_indices = np.argsort(row)[::-1][:5]
        keywords = [terms[j] for j in top_indices]

        updated_cluster = cluster.model_copy(update={
            "keywords": keywords,
            "label": " / ".join(keywords[:3]),
            "labeling_method": "ctfidf"
        })

        updated_clusters.append(updated_cluster)

    return updated_clusters

