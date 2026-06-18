import numpy as np
from bertopic import BERTopic
from bertopic.representation import OpenAI as BERTopicOpenAI
from umap import UMAP
from hdbscan import HDBSCAN
from openai import OpenAI
from dotenv import load_dotenv

from sklearn.feature_extraction.text import CountVectorizer

from pipeline.config import IMBALANCE_THRESHOLD
from pipeline.schemas import Cluster, JournalEntry, TopicAssignment

load_dotenv()

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
        min_cluster_size = 10,
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

    representation_model = BERTopicOpenAI(OpenAI(), model="gpt-4o-mini", chat=True)

    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer,
        representation_model=representation_model,
        nr_topics="auto",
        min_topic_size=5,
        verbose=False,
    )
    return topic_model, umap_model, hdbscan_model, representation_model

def run(entries: list[JournalEntry], embeddings: np.ndarray) -> list[TopicAssignment]:
    docs = [e.text for e in entries]

    topic_model, _, _, representation_model = build_models(len(docs))

    topics, probs = topic_model.fit_transform(docs, embeddings)

    topics = topic_model.reduce_outliers(docs, topics, probabilities=probs, strategy="probabilities")

    topic_model.update_topics(docs, topics=topics, representation_model=representation_model)

    topic_info = topic_model.get_topic_info()
    topic_names = dict(zip(topic_info["Topic"], topic_info["Name"]))

    all_topic_assignments = []

    for i, (entry, topic_id, prob_row) in enumerate(zip(entries, topics, probs)):
        raw_keywords = topic_model.get_topic(topic_id)
        keywords = [word for word, score in raw_keywords[:5]] if raw_keywords else []

        topic_assignment = TopicAssignment(
            entry_id=entry.id,
            topic_id=topic_id,
            keywords=keywords,
            topic_label=topic_names.get(topic_id, f"topic_{topic_id}"),
            probability=float(probs[i].max())
        )

        all_topic_assignments.append(topic_assignment)

    return all_topic_assignments

def assignments_to_clusters(assignments: list[TopicAssignment]) -> list[Cluster]:
    from collections import defaultdict
    from pipeline.schemas import Cluster

    groups = defaultdict(list)
    for a in assignments:
        groups[a.topic_id].append(a)

    clusters = []
    for topic_id, group in groups.items():
        if topic_id == -1:
            continue

        entry_ids = [a.entry_id for a in group]
        sorted_group = sorted(group, key=lambda a: a.probability, reverse=True)
        representative_entry_ids = [a.entry_id for a in sorted_group[:3]]

        raw_label = group[0].topic_label
        label = raw_label.split("_", 1)[1] if "_" in raw_label else raw_label

        cluster = Cluster(
            cluster_id=topic_id,
            entry_ids=entry_ids,
            representative_entry_ids=representative_entry_ids,
            label=label,
            keywords=group[0].keywords,
            labeling_method="bertopic"
        )
        clusters.append(cluster)

    total = len(assignments)

    for cluster in clusters:
        share = len(cluster.entry_ids) / total

        if share > IMBALANCE_THRESHOLD:
            print(
                f"[WARNING] cluster {cluster.cluster_id} contains {share:.1%} of entries "
                f"— possible catch-all. Run isolation sub-clustering to check for "
                f"real substructure before interpreting this as a coherent theme."
            )

    return clusters
