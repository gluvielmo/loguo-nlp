import json
from statistics import mean
from datetime import datetime

from pipeline.embeddings.embedder import _get_client
from pipeline.schemas import Cluster, JournalEntry, LinguisticFeatures, Report, Theme


def generate(
        condition_name: str,
        entries: list[JournalEntry],
        clusters: list[Cluster],
        lfe_list: list[LinguisticFeatures]
) -> tuple[Report, int, int]:
    corpus_size = len(entries)
    date_range = (min(e.date for e in entries), max(e.date for e in entries))
    generated_at = datetime.utcnow()

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

    Respond with a JSON object with exactly these keys:
    - "temporal_evolution": a dict mapping period names to descriptions of how themes shifted (e.g. {{"2009-2012": "...", "2013-2017": "...", "2018-2023": "..."}})
    - "surprising_patterns": a list of 3-5 strings describing unexpected findings
    - "reflection_questions": a list of 5 questions the journaler might reflect on based on these patterns
    - "limitations": a list of 2-3 strings describing limitations of this analysis
    """
            }
        ]
    )

    data = json.loads(response.choices[0].message.content)
    usage = response.usage

    return Report(
        condition_name=condition_name,
        corpus_size=corpus_size,
        date_range=date_range,
        generated_at=generated_at,
        main_themes=main_themes,
        subthemes=subthemes,
        temporal_evolution=data["temporal_evolution"],
        linguistic_patterns=linguistic_patterns,
        representative_evidence=representative_evidence,
        surprising_patterns=data["surprising_patterns"],
        reflection_questions=data["reflection_questions"],
        limitations=data["limitations"],
    ), usage.prompt_tokens, usage.completion_tokens
