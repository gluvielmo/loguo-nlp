import json
from pathlib import Path

from pipeline.schemas import ConditionArtifacts


def load_artifacts(run_dir: str | Path) -> ConditionArtifacts:
    path = Path(run_dir) / "artifacts.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return ConditionArtifacts.model_validate(data)


def compare(run_dirs: list[str | Path]) -> None:
    all_artifacts = [load_artifacts(d) for d in run_dirs]

    print(f"\n{'=' * 60}")
    print("CONDITION COMPARISON")
    print(f"{'=' * 60}\n")

    print(f"{'Condition':<35} {'Entries':<10} {'Themes':<10} {'Runtime'}")
    print("-" * 65)
    for a in all_artifacts:
        r = a.report
        print(
            f"{a.condition:<35} "
            f"{r.corpus_size:<10} "
            f"{len(r.main_themes):<10} "
            f"{a.runtime_seconds:.1f}s"
        )

    print(f"\n{'=' * 60}")
    print("MAIN THEMES PER CONDITION")
    print(f"{'=' * 60}")
    for a in all_artifacts:
        print(f"\n[{a.condition}]")
        for theme in a.report.main_themes[:5]:
            print(f"  - {theme.name}")

    print(f"\n{'=' * 60}")
    print("SURPRISING PATTERNS")
    print(f"{'=' * 60}")
    for a in all_artifacts:
        print(f"\n[{a.condition}]")
        for p in a.report.surprising_patterns[:3]:
            print(f"  • {p}")

    print(f"\n{'=' * 60}")
    print("REFLECTION QUESTIONS")
    print(f"{'=' * 60}")
    for a in all_artifacts:
        print(f"\n[{a.condition}]")
        for i, q in enumerate(a.report.reflection_questions[:3], 1):
            print(f"  {i}. {q}")
