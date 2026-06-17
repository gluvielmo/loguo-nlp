import json
from statistics import mean
from datetime import datetime

from pipeline.embeddings.embedder import _get_client
from pipeline.schemas import Cluster, JournalEntry, LinguisticFeatures, Report, Theme, TemporalAnalysis
from pipeline.temporal.analyzer import bucket_entries, corpus_temporal, theme_temporal
from pipeline.config import STABILITY_BAND

def _theme_shares_per_bin(
    clusters: list[Cluster],
    buckets: dict[str, list[str]],
) -> dict[str, dict[str, float]]:
    result = {}
    for cluster in clusters:
        cluster_ids = set(cluster.entry_ids)

        result[cluster.label] = {
            period: sum(1 for eid in bin_ids if eid in cluster_ids) / len(bin_ids)
            for period, bin_ids in buckets.items()
            if bin_ids
        }

    return result

def _classify_stability(
    theme_shares: dict[str, dict[str, float]],
    band: float = STABILITY_BAND,
) -> dict[str, bool]:
    result = {}
    for theme, shares in theme_shares.items():
        values = list(shares.values())
        result[theme] = len(values) < 2 or (max(values) - min(values)) <= band

    return result


def _to_str_list(items: list) -> list[str]:
    return [json.dumps(item) if isinstance(item, dict) else str(item) for item in items]


def _format_bin(period: str, p) -> str:
    lines = [
        f"{period} | {p.entry_count} entries | avg {p.mean_word_count:.0f} words",
        f"  ratios: 1st-person {p.first_person_ratio:.3f}"
        f" | negation {p.negation_rate:.3f}"
        f" | uncertainty {p.uncertainty_rate:.3f}"
        f" | pressure {p.pressure_word_rate:.3f}"
        f" | difficulty {p.difficulty_rate:.3f}"
        f" | crisis {p.crisis_indicator_rate:.3f}",
        f"  voice/tense: passive {p.passive_voice_rate:.3f}"
        f" | active {p.active_voice_rate:.3f}"
        f" | past_tense {p.past_tense_rate:.3f}",
        f"  questions: direct_rate {p.direct_question_rate:.3f}"
        f" | deliberative_rate {p.deliberative_question_rate:.3f}",
        f"  raw counts: crisis={p.crisis_indicator_count}"
        f" | direct_q={p.direct_question_count}"
        f" | delib_q={p.deliberative_question_count}",
    ]
    if p.top_predicate_adjectives:
        lines.append(f"  top_adj: {', '.join(p.top_predicate_adjectives)}")
    if p.top_uncertainty_terms:
        lines.append(f"  top_uncertainty: {', '.join(p.top_uncertainty_terms)}")
    if p.top_negation_terms:
        lines.append(f"  top_negation: {', '.join(p.top_negation_terms)}")
    if p.top_named_entities:
        lines.append(f"  top_entities: {', '.join(p.top_named_entities)}")
    if p.top_temporal_expressions:
        lines.append(f"  top_temporal: {', '.join(p.top_temporal_expressions)}")
    return "\n".join(lines)


_SYSTEM_PROMPT = (
    "You are an expert in longitudinal analysis of personal writing. "
    "Write exclusively in second person (\"you wrote...\", \"your entries...\", \"your writing...\"). "
    "Your role is to describe and analyze patterns in the corpus — not to advise. "
    "Never use phrases like \"you should\", \"you might consider\", \"it would be helpful to\", "
    "\"this suggests you would benefit from\", or any construction that implies what the writer "
    "should do, even when softened or embedded in an otherwise descriptive sentence. "
    "If a finding has an obvious actionable implication, state the finding only — not the implied action. "
    "Hedge all interpretive claims: use language like \"this may suggest...\", "
    "\"this could reflect...\", or \"one possible reading is...\". "
    "Psychological interpretation must be explicitly marked as speculative."
    "Distinguish between what was journaled about and the person's life or identity more broadly. "
    "Do not write 'this person's life revolved around X' or 'X defined their identity' — "
    "prefer 'the journaling during this period centered on X' or 'your entries in this period "
    "focused heavily on X'."

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

    theme_shares = _theme_shares_per_bin(clusters, buckets) if clusters else {}
    theme_stability = _classify_stability(theme_shares)

    stable_themes  = [t for t, s in theme_stability.items() if s]
    dynamic_themes = [t for t, s in theme_stability.items() if not s]

    if theme_shares:
        stability_lines = []
        if stable_themes:
            stability_lines.append(
                f"Stable themes (share varies ≤10pp across all bins): "
                f"{', '.join(stable_themes)}"
            )
        if dynamic_themes:
            stability_lines.append(
                f"Dynamic themes (share varies >10pp): "
                f"{', '.join(dynamic_themes)}"
            )
        stability_context = "\n".join(stability_lines)
    else:
        stability_context = ""


    corpus_prof = corpus_temporal(entries, lfe_list, buckets) if lfe_list else {}
    theme_prof = theme_temporal(clusters, lfe_list, buckets) if lfe_list and clusters else {}

    if corpus_prof:
        corpus_lines = "\n".join(_format_bin(period, p) for period, p in corpus_prof.items())
        corpus_temporal_section = f"Corpus-level LFE by bin:\n{corpus_lines}"
    else:
        corpus_temporal_section = "No LFE data available — linguistic register metrics are not included."

    if theme_prof:
        top_cluster_labels = {
            c.label for c in sorted(clusters, key=lambda c: len(c.entry_ids), reverse=True)[:5]
        }
        theme_lines = []
        for theme, periods in theme_prof.items():
            if theme not in top_cluster_labels:
                continue
            theme_lines.append(f"Theme: {theme}")
            for period, prof in periods.items():
                theme_lines.append(f"  {_format_bin(period, prof)}")
        theme_temporal_section = "Theme-level LFE by bin (top 5 themes by size):\n" + "\n".join(theme_lines)
    else:
        theme_temporal_section = ""

    temporal_context = corpus_temporal_section
    if theme_temporal_section:
        temporal_context += "\n\n" + theme_temporal_section

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
        lfe_context = f"""Corpus-wide LFE averages:
  - Words per entry: {linguistic_patterns['avg_word_count']}
  - Negations per entry: {linguistic_patterns['avg_negation_count']}
  - First-person pronoun ratio: {linguistic_patterns['avg_first_person_ratio']}"""
    else:
        linguistic_patterns = {}
        lfe_context = "No linguistic feature extraction was applied to this condition."

    if clusters:
        total_entries = sum(len(c.entry_ids) for c in clusters)
        theme_summary = "\n".join(
            f"  - {c.label}: {len(c.entry_ids)} entries"
            f" ({len(c.entry_ids)/total_entries*100:.1f}%) — {c.description[:120]}"
            for c in sorted(clusters, key=lambda c: len(c.entry_ids), reverse=True)
        )
        theme_context = f"Themes (sorted by size):\n{theme_summary}"
    else:
        theme_context = "No topic structure applied — entries were not clustered."

    context = f"""Corpus: {corpus_size} journal entries spanning {date_range[0]} to {date_range[1]}.
Condition: {condition_name}

{theme_context}

{lfe_context}"""

    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Analyze this longitudinal journal corpus and produce a structured interpretive report.

{context}

=== Temporal LFE Profiles ===
{temporal_context}

Respond with a JSON object containing exactly these keys:

"corpus_overview"
A single prose paragraph (second person) covering:
- Total volume and time span
- Dominant theme(s) by approximate proportion of entries
- Notable minority or marginal themes — not just the largest clusters
- Overall compositional character

=== Theme Stability ===
{stability_context}

For STABLE themes listed above:
- Do not repeat their share month-by-month. State the sustained focus once, clearly.
- Then check whether the LFE signature (linguistic_register) actually varied even though the share did not. If it did, describe that shift.
- If both share and LFE are flat, say so directly: "sustained focus with little change in either content or linguistic register." That is a complete and valid finding — do not pad it.

For DYNAMIC themes listed above:
- Describe the arc normally: how share shifted across periods, and how LFE moved with it.

"temporal_arc"
A list of objects, one per time bin listed above, in chronological order.
Merge adjacent bins with fewer than 10 entries into a single object rather than reporting them separately.
Each object must have exactly:
  "period": the bin label (e.g. "early", "2012-06", "2009–2012")
  "theme_composition": 1–2 sentences following the stable/dynamic rules above.
  "linguistic_register": 1–2 sentences on how the writing style shifted in this period, citing specific LFE metrics and their values from the data above (e.g. first-person ratio, negation rate, uncertainty rate, past-tense rate, pressure-word rate). If no LFE data is available for this condition, state that explicitly in this field.

"synthesis"
A single closing paragraph connecting dominant themes to linguistic register patterns over time.
Example form: "The cluster focused on X coincided with elevated negation rates (0.031) during mid-2013, which may suggest..."
Mark any psychological interpretation as speculative. Do not offer advice, recommendations, or any prescriptive language.

"limitations"
A list of 2–3 strings identifying genuine limitations of this analysis — e.g. data gaps, cluster boundary ambiguity, LFE metric confounds.
"""
            }
        ]
    )

    data = json.loads(response.choices[0].message.content)

    temporal_analysis = TemporalAnalysis(
        corpus_overview=str(data.get("corpus_overview", "")),
        temporal_arc=data.get("temporal_arc", []),
        synthesis=str(data.get("synthesis", "")),
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
        limitations=_to_str_list(data.get("limitations", [])),
    ), usage.prompt_tokens, usage.completion_tokens
