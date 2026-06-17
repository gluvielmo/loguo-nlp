from __future__ import annotations

import json
from pathlib import Path

from pipeline.schemas import ConditionArtifacts


def save(artifacts: ConditionArtifacts, output_dir: str | Path = "outputs") -> Path:
    output_dir = Path(output_dir)
    run_id = artifacts.run_timestamp.strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / f"{run_id}_{artifacts.condition}"
    run_dir.mkdir(parents=True, exist_ok=True)

    json_path = run_dir / "artifacts.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(artifacts.model_dump(mode="json"), f, indent=2, default=str)

    md_path = run_dir / "report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_to_markdown(artifacts))

    print(f"Saved to {run_dir}")
    return run_dir


def _to_markdown(artifacts: ConditionArtifacts) -> str:
    r = artifacts.report
    lines = [
        "# Longitudinal Journal Analysis",
        "",
        f"**Condition:** {r.condition_name}  ",
        f"**Corpus size:** {r.corpus_size} entries  ",
        f"**Date range:** {r.date_range[0]} → {r.date_range[1]}  ",
        f"**Generated at:** {r.generated_at}  ",
        "",
        "## Run Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total runtime | {artifacts.metrics.total_seconds:.1f}s |",
        f"| Preprocessing (local) | {artifacts.metrics.preprocessing_seconds:.1f}s |",
        f"| LLM time | {artifacts.metrics.llm_seconds:.1f}s |",
        f"| LLM calls | {artifacts.metrics.llm_calls} |",
        f"| Input tokens | {artifacts.metrics.input_tokens:,} |",
        f"| Output tokens | {artifacts.metrics.output_tokens:,} |",
        f"| Embedding tokens | {artifacts.metrics.embedding_tokens:,} ({artifacts.metrics.embedding_entries} entries) |",
        f"| Embedding model | {artifacts.metrics.embedding_model or 'n/a'} |",
        f"| Generation model | {artifacts.metrics.generation_model} |",
        f"| Estimated cost | ${artifacts.metrics.estimated_cost_usd:.4f} |",
        "",
        "---",
        "",
        "## Main Themes",
        "",
    ]

    for theme in r.main_themes:
        lines.append(f"### {theme.name}")
        if theme.description:
            lines.append(theme.description)
        lines.append("")

    if r.subthemes:
        lines += ["## Subthemes", ""]
        for sub in r.subthemes:
            lines.append(f"- **{sub.name}**" + (f": {sub.description}" if sub.description else ""))
        lines.append("")

    if r.temporal_analysis:
        ta = r.temporal_analysis
        lines += ["## Patterns & Analysis", ""]

        if ta.corpus_overview:
            lines += ["### Corpus Overview", "", ta.corpus_overview, ""]

        if ta.temporal_arc:
            lines += ["### Temporal Arc", ""]
            for bin_entry in ta.temporal_arc:
                period = bin_entry.get("period", "")
                lines.append(f"**{period}**")
                if tc := bin_entry.get("theme_composition"):
                    lines += ["", tc]
                if lr := bin_entry.get("linguistic_register"):
                    lines += ["", f"*{lr}*"]
                lines.append("")

        if ta.synthesis:
            lines += ["### Synthesis", "", ta.synthesis, ""]

    if r.linguistic_patterns:
        lines += ["## Linguistic Patterns", ""]
        for key, value in r.linguistic_patterns.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    if r.limitations:
        lines += ["## Limitations", ""]
        for lim in r.limitations:
            lines.append(f"- {lim}")

    return "\n".join(lines)
