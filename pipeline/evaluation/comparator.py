from __future__ import annotations

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
    lines += ["| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |"]
    lines += ["|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|"]
    for a in all_artifacts:
        m = a.metrics
        lines.append(
            f"| {a.condition} | {a.report.corpus_size} | {len(a.report.main_themes)} "
            f"| {m.total_seconds:.1f}s | {m.preprocessing_seconds:.1f}s "
            f"| {m.llm_calls} | {m.input_tokens:,} | {m.output_tokens:,} "
            f"| {m.embedding_tokens:,} | ${m.estimated_cost_usd:.4f} |"
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
