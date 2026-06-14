import numpy as np
from collections import defaultdict

from sklearn.cluster import AgglomerativeClustering

from pipeline.schemas import JournalEntry, Cluster

def run(entries: list[JournalEntry], embeddings: np.ndarray, n_clusters: int = 10) -> list[Cluster]:
    model = AgglomerativeClustering(n_clusters=n_clusters, metric="cosine", linkage="average")

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

    return clusters