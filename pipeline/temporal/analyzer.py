from collections import Counter
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


def _top_terms(lfes: list[LinguisticFeatures], field: str, n: int = 5) -> list[str]:
    all_terms = []
    for lfe in lfes:
        all_terms.extend(getattr(lfe, field, []))
    return [term for term, _ in Counter(all_terms).most_common(n)]


def _bin_profile(entry_ids: list[str], lfe_by_id: dict[str, LinguisticFeatures]) -> BinProfile:
    lfes = [lfe_by_id[eid] for eid in entry_ids if eid in lfe_by_id]

    if not lfes:
        return BinProfile(
            entry_count=0,
            mean_word_count=0.0,
            negation_rate=0.0,
            uncertainty_rate=0.0,
            pressure_word_rate=0.0,
            difficulty_rate=0.0,
            crisis_indicator_rate=0.0,
            first_person_ratio=0.0,
            passive_voice_rate=0.0,
            active_voice_rate=0.0,
            past_tense_rate=0.0,
            direct_question_rate=0.0,
            deliberative_question_rate=0.0,
            crisis_indicator_count=0,
            direct_question_count=0,
            deliberative_question_count=0,
        )

    word_counts     = [f.word_count for f in lfes]
    sentence_counts = [f.sentence_count for f in lfes]

    def _word_rate(counts):
        return mean(c / w for c, w in zip(counts, word_counts) if w > 0)

    def _sentence_rate(counts):
        return mean(c / s for c, s in zip(counts, sentence_counts) if s > 0)

    return BinProfile(
        entry_count=len(lfes),
        mean_word_count=mean(word_counts),
        negation_rate=_word_rate([f.negation_count for f in lfes]),
        uncertainty_rate=_word_rate([f.uncertainty_word_count for f in lfes]),
        pressure_word_rate=_word_rate([f.pressure_word_count for f in lfes]),
        difficulty_rate=_word_rate([f.difficulty_count for f in lfes]),
        crisis_indicator_rate=_word_rate([f.crisis_indicator_count for f in lfes]),
        first_person_ratio=mean(f.first_person_pronoun_ratio for f in lfes),
        passive_voice_rate=_word_rate([f.passive_voice_count for f in lfes]),
        active_voice_rate=_word_rate([f.active_voice_count for f in lfes]),
        past_tense_rate=_word_rate([f.past_tense_count for f in lfes]),
        direct_question_rate=_sentence_rate([f.direct_question_count for f in lfes]),
        deliberative_question_rate=_sentence_rate([f.deliberative_question_count for f in lfes]),
        crisis_indicator_count=sum(f.crisis_indicator_count for f in lfes),
        direct_question_count=sum(f.direct_question_count for f in lfes),
        deliberative_question_count=sum(f.deliberative_question_count for f in lfes),
        top_predicate_adjectives=_top_terms(lfes, "predicate_adjectives"),
        top_uncertainty_terms=_top_terms(lfes, "uncertainty_terms"),
        top_negation_terms=_top_terms(lfes, "negation_terms"),
        top_named_entities=_top_terms(lfes, "named_entities"),
        top_temporal_expressions=_top_terms(lfes, "temporal_expressions"),
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
