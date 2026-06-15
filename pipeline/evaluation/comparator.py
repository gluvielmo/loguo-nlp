import json
from pathlib import Path

from pipeline.schemas import ConditionArtifacts


def load_artifacts(run_dir: str | Path) -> ConditionArtifacts:
    path = Path(run_dir) / "artifacts.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return ConditionArtifacts.model_validate(data)


def compare(run_dirs: list[str | Path], output_path: str | Path = "outputs/comparison.md") -> Path:
    all_artifacts = [load_artifacts(d) for d in run_dirs]
    lines = []

    lines += ["# Condition Comparison", ""]

    lines += ["## Summary", ""]
    lines += [f"| {'Condition':<33} | {'Entries':<7} | {'Themes':<6} | Runtime |"]
    lines += [f"|{'-'*35}|{'-'*9}|{'-'*8}|---------|"]
    for a in all_artifacts:
        r = a.report
        lines.append(
            f"| {a.condition:<33} | {r.corpus_size:<7} | {len(r.main_themes):<6} | {a.runtime_seconds:.1f}s |"
        )

    lines += ["", "## Main Themes", ""]
    for a in all_artifacts:
        lines.append(f"### [{a.condition}]")
        for theme in a.report.main_themes[:5]:
            lines.append(f"- {theme.name}")
        lines.append("")

    lines += ["## Surprising Patterns", ""]
    for a in all_artifacts:
        lines.append(f"### [{a.condition}]")
        for p in a.report.surprising_patterns[:3]:
            lines.append(f"- {p}")
        lines.append("")

    lines += ["## Reflection Questions", ""]
    for a in all_artifacts:
        lines.append(f"### [{a.condition}]")
        for i, q in enumerate(a.report.reflection_questions[:3], 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Comparison saved to {output_path}")
    return output_path
