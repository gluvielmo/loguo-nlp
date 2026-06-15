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
        f"**Runtime:** {artifacts.runtime_seconds:.1f}s  ",
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

    if r.temporal_evolution:
        lines += ["## Temporal Evolution", ""]
        for period, description in r.temporal_evolution.items():
            lines.append(f"**{period}:** {description}")
            lines.append("")

    if r.linguistic_patterns:
        lines += ["## Linguistic Patterns", ""]
        for key, value in r.linguistic_patterns.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    if r.surprising_patterns:
        lines += ["## Surprising Patterns", ""]
        for p in r.surprising_patterns:
            lines.append(f"- {p}")
        lines.append("")

    if r.reflection_questions:
        lines += ["## Reflection Questions", ""]
        for i, q in enumerate(r.reflection_questions, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    if r.limitations:
        lines += ["## Limitations", ""]
        for lim in r.limitations:
            lines.append(f"- {lim}")

    return "\n".join(lines)
