from statistics import mean

from pipeline.schemas import BinProfile, Cluster, JournalEntry, LinguisticFeatures


def bucket_entries(entries: list[JournalEntry]) -> dict[str, list[str]]:
    sorted_entries = sorted(entries, key=lambda e: e.date)

    if len(entries) < 50:
        n = len(sorted_entries)
        return {
            "early": [e.id for e in sorted_entries[:n // 3]],
            "mid":   [e.id for e in sorted_entries[n // 3:2 * n // 3]],
            "late":  [e.id for e in sorted_entries[2 * n // 3:]],
        }

    buckets: dict[str, list[str]] = {}
    for e in sorted_entries:
        key = f"{e.date.year}-{e.date.month:02d}"
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(e.id)

    return buckets


def _bin_profile(entry_ids: list[str], lfe_by_id: dict[str, LinguisticFeatures]) -> BinProfile:
    lfes = [lfe_by_id[eid] for eid in entry_ids if eid in lfe_by_id]

    if not lfes:
        return BinProfile(
            entry_count=0,
            mean_word_count=0.0,
            negation_rate=0.0,
            uncertainty_rate=0.0,
            first_person_ratio=0.0,
            direct_question_rate=0.0,
            deliberative_question_rate=0.0,
            past_tense_rate=0.0,
        )

    word_counts      = [f.word_count for f in lfes]
    sentence_counts  = [f.sentence_count for f in lfes]

    def _word_rate(counts):
        return mean(c / w for c, w in zip(counts, word_counts) if w > 0)

    def _sentence_rate(counts):
        return mean(c / s for c, s in zip(counts, sentence_counts) if s > 0)

    return BinProfile(
        entry_count=len(lfes),
        mean_word_count=mean(word_counts),
        negation_rate=_word_rate([f.negation_count for f in lfes]),
        uncertainty_rate=_word_rate([f.uncertainty_word_count for f in lfes]),
        first_person_ratio=mean(f.first_person_pronoun_ratio for f in lfes),
        direct_question_rate=_sentence_rate([f.direct_question_count for f in lfes]),
        deliberative_question_rate=_sentence_rate([f.deliberative_question_count for f in lfes]),
        past_tense_rate=_word_rate([f.past_tense_count for f in lfes]),
    )


def corpus_temporal(
    entries: list[JournalEntry],
    lfe_list: list[LinguisticFeatures],
    buckets: dict[str, list[str]],
) -> dict[str, BinProfile]:
    lfe_by_id = {f.entry_id: f for f in lfe_list}
    return {
        period: _bin_profile(ids, lfe_by_id)
        for period, ids in buckets.items()
    }


def theme_temporal(
    clusters: list[Cluster],
    lfe_list: list[LinguisticFeatures],
    buckets: dict[str, list[str]],
) -> dict[str, dict[str, BinProfile]]:
    lfe_by_id = {f.entry_id: f for f in lfe_list}

    result = {}
    for cluster in clusters:
        cluster_ids = set(cluster.entry_ids)
        result[cluster.label] = {}

        for period, ids in buckets.items():
            intersection = [eid for eid in ids if eid in cluster_ids]
            if not intersection:
                continue
            result[cluster.label][period] = _bin_profile(intersection, lfe_by_id)

    return result
