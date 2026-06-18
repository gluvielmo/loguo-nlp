import numpy as np
from collections import defaultdict

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize

from pipeline.config import IMBALANCE_THRESHOLD
from pipeline.schemas import JournalEntry, Cluster

def _pick_n_clusters(
    embeddings: np.ndarray,
    candidates: list[int],
    metric: str = "cosine",
    linkage: str = "complete",
) -> tuple[int, float]:
    normalized = normalize(embeddings)
    best_k, best_score = candidates[0], -1.0
    for k in candidates:
        labels = AgglomerativeClustering(
            n_clusters=k, metric=metric, linkage=linkage
        ).fit_predict(embeddings)
        score = silhouette_score(normalized, labels, metric="euclidean")
        if score > best_score:
            best_score = score
            best_k = k
    return best_k, best_score


def run(entries: list[JournalEntry], embeddings: np.ndarray, n_clusters: int | None = None) -> list[Cluster]:
    if n_clusters is None:
        n_clusters, sil = _pick_n_clusters(embeddings, [3, 5, 7, 10, 15, 20])
        print(f"[hierarchical] auto-selected k={n_clusters} (silhouette={sil:.3f})")

    
    model = AgglomerativeClustering(n_clusters=n_clusters, metric="cosine", linkage="complete")

    labels = model.fit_predict(embeddings)

    cluster_to_indices = defaultdict(list)

    for i, label in enumerate(labels):
        cluster_to_indices[label].append(i)

    clusters = []

    for cluster_id in range(n_clusters):
        indices = cluster_to_indices[cluster_id]
        cluster_vecs = embeddings[indices]

        centroid = cluster_vecs.mean(axis=0)
        distances = np.linalg.norm(cluster_vecs - centroid, axis=1)
        closest = np.argsort(distances)[:3]

        cluster = Cluster(
            cluster_id=cluster_id,
            entry_ids=[entries[i].id for i in indices],
            representative_entry_ids=[entries[indices[j]].id for j in closest],
            label=f"cluster_{cluster_id}",
            labeling_method="pending",
            keywords=[]
        )

        clusters.append(cluster)

    total = len(entries)

    for cluster in clusters:
        share = len(cluster.entry_ids) / total

        if share > IMBALANCE_THRESHOLD:
            print(
                f"[WARNING] cluster {cluster.cluster_id} contains {share:.1%} of entries "
                f"— possible catch-all. Run isolation sub-clustering to check for "
                f"real substructure before interpreting this as a coherent theme."
            )

    return clusters