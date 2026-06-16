import json
from statistics import mean
from datetime import datetime

from pipeline.embeddings.embedder import _get_client
from pipeline.schemas import Cluster, JournalEntry, LinguisticFeatures, Report, Theme, TemporalAnalysis
from pipeline.temporal.analyzer import bucket_entries, corpus_temporal, theme_temporal

def _to_str_list(items: list) -> list[str]:
    return [json.dumps(item) if isinstance(item, dict) else str(item) for item in items]


def _format_bin(period: str, p) -> str:
    return (
        f"{period} | {p.entry_count} entries | avg {p.mean_word_count:.0f} words"
        f" | negation {p.negation_rate:.3f}"
        f" | uncertainty {p.uncertainty_rate:.3f}"
        f" | 1st-person {p.first_person_ratio:.3f}"
        f" | direct_q {p.direct_question_rate:.3f}"
        f" | deliberative_q {p.deliberative_question_rate:.3f}"
        f" | past_tense {p.past_tense_rate:.3f}"
    )


def generate(
        condition_name: str,
        entries: list[JournalEntry],
        clusters: list[Cluster],
        lfe_list: list[LinguisticFeatures]
) -> tuple[Report, int, int]:
    corpus_size = len(entries)
    date_range = (min(e.date for e in entries), max(e.date for e in entries))
    generated_at = datetime.utcnow()

    buckets = bucket_entries(entries)
    corpus_prof = corpus_temporal(entries, lfe_list, buckets) if lfe_list else {}
    theme_prof = theme_temporal(clusters, lfe_list, buckets) if lfe_list and clusters else {}

    if corpus_prof:
        corpus_lines = "\n".join(_format_bin(period, p) for period, p in corpus_prof.items())
        corpus_temporal_analysis = f"Corpus temporal analysis:\n{corpus_lines}"
    else:
        corpus_temporal_analysis = "No temporal analysis applied to the corpus."

    if theme_prof:
        theme_lines = []
        for theme, periods in theme_prof.items():
            theme_lines.append(f"Theme: {theme}")
            for period, prof in periods.items():
                theme_lines.append(f"  {_format_bin(period, prof)}")

        theme_temporal_analysis = "Theme temporal analysis:\n" + "\n".join(theme_lines)

    main_themes = [
        Theme(name=c.label, description=c.description, entry_ids=c.entry_ids) for c in clusters
    ]

    subthemes = [
        Theme(name=sub, description="", entry_ids=[])
        for c in clusters
        for sub in c.subthemes
    ]

    representative_evidence = [
        {"entry_id": eid, "cluster_label": c.label}
        for c in clusters
        for eid in c.representative_entry_ids
    ]

    if lfe_list:
        linguistic_patterns = {
            "avg_word_count": round(mean(f.word_count for f in lfe_list), 1),
            "avg_negation_count": round(mean(f.negation_count for f in lfe_list), 2),
            "avg_first_person_ratio": round(mean(f.first_person_pronoun_ratio for f in lfe_list), 4),
            "avg_sentence_count": round(mean(f.sentence_count for f in lfe_list), 1),
        }
        lfe_context = f"""Linguistic patterns (averages):
    - Words per entry: {linguistic_patterns['avg_word_count']}
    - Negations per entry: {linguistic_patterns['avg_negation_count']}
    - First-person pronoun ratio: {linguistic_patterns['avg_first_person_ratio']}"""
    else:
        linguistic_patterns = {}
        lfe_context = "No linguistic feature extraction was applied."

    if clusters:
        theme_summary = "\n".join(
            f"- {c.label}: {len(c.entry_ids)} entries ({c.description[:100]})"
            for c in clusters
        )
        theme_context = f"Themes discovered:\n    {theme_summary}"
    else:
        theme_context = "No topic structure applied — entries were not clustered."

    context = f"""Corpus: {corpus_size} journal entries from {date_range[0]} to {date_range[1]}.
    Condition: {condition_name}

    {theme_context}

    {lfe_context}
    """

    temporal_context = corpus_temporal_analysis

    if theme_prof:
        temporal_context += "\n\n" + theme_temporal_analysis


    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert in longitudinal analysis of personal writing and psychological patterns."
            },
            {
                "role": "user",
                "content": f"""Based on this journal corpus analysis, provide interpretive insights.

                            {context}

                            === Temporal LFE Profiles ===
                            {temporal_context}

                            Using the LFE data above, respond with a JSON object with exactly these keys:
                            - "emerging_themes": list of strings — themes that grow in frequency or intensity over time
                            - "declining_themes": list of strings — themes that shrink or fade
                            - "persistent_themes": list of strings — themes stable across the full time range
                            - "cyclical_themes": list of strings — themes that disappeared and returned
                            - "framing_shifts": list of strings, each a complete sentence describing how emotional or linguistic framing changed within a theme over time. Cite specific LFE metrics and periods. Example: ["The Parenting cluster shifted from humor in 2009 to exhaustion by 2015, reflected in rising negation rates (0.018 → 0.031)"]
                            - "turning_points": list of strings, each a complete sentence identifying a specific period where something shifted noticeably, with evidence. Example: ["2012-06 shows a spike in uncertainty rate (0.041) across the Depression cluster, suggesting a period of heightened doubt"]
                            - "early_evidence": list of strings — notable patterns from the earliest period
                            - "late_evidence": list of strings — notable patterns from the most recent period
                            - "uncertainty_notes": list of strings — limitations or alternative explanations for what you observed
                            - "period_summaries": dict mapping period labels to a one-sentence description of that period
                            - "surprising_patterns": list of 3-5 strings describing unexpected findings
                            - "reflection_questions": list of 5 questions the journaler might reflect on
                            - "limitations": list of 2-3 strings describing limitations of this analysis
                            """
            }
        ]
    )

    data = json.loads(response.choices[0].message.content)

    temporal_analysis = TemporalAnalysis(
        emerging_themes=_to_str_list(data.get("emerging_themes", [])),
        declining_themes=_to_str_list(data.get("declining_themes", [])),
        persistent_themes=_to_str_list(data.get("persistent_themes", [])),
        cyclical_themes=_to_str_list(data.get("cyclical_themes", [])),
        framing_shifts=_to_str_list(data.get("framing_shifts", [])),
        turning_points=_to_str_list(data.get("turning_points", [])),
        early_evidence=_to_str_list(data.get("early_evidence", [])),
        late_evidence=_to_str_list(data.get("late_evidence", [])),
        uncertainty_notes=_to_str_list(data.get("uncertainty_notes", [])),
        period_summaries=data.get("period_summaries", {}),
    )

    usage = response.usage

    return Report(
        condition_name=condition_name,
        corpus_size=corpus_size,
        date_range=date_range,
        generated_at=generated_at,
        main_themes=main_themes,
        subthemes=subthemes,
        temporal_analysis=temporal_analysis,
        linguistic_patterns=linguistic_patterns,
        representative_evidence=representative_evidence,
        surprising_patterns=data["surprising_patterns"],
        reflection_questions=data["reflection_questions"],
        limitations=data["limitations"],
    ), usage.prompt_tokens, usage.completion_tokens
