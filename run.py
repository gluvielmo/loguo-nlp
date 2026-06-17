import argparse
from pathlib import Path

ALL_CONDITIONS = list("ABCDE")
_USES_N_CLUSTERS = set("DE")


def run_condition(condition: str, csv: str, source: str, output: str, n_clusters: int) -> Path:
    from pipeline.artifacts.saver import save

    if condition == "A":
        from conditions.condition_a import run
    elif condition == "B":
        from conditions.condition_b import run
    elif condition == "C":
        from conditions.condition_c import run
    elif condition == "D":
        from conditions.condition_d import run
    elif condition == "E":
        from conditions.condition_e import run

    if condition in _USES_N_CLUSTERS:
        artifacts = run(csv, source=source, n_clusters=n_clusters)
    else:
        artifacts = run(csv, source=source)

    run_dir = save(artifacts, output_dir=output)
    print(f"Condition {condition} complete → {run_dir}")
    return run_dir


def main():
    parser = argparse.ArgumentParser(description="Longitudinal journal analysis pipeline")
    parser.add_argument("--condition", type=str, choices=ALL_CONDITIONS,
                        help="Which condition to run (A–E). Omit to run all 5.")
    parser.add_argument("--csv", type=str, default="data/dooce_2009_2023.csv",
                        help="Path to the corpus CSV file")
    parser.add_argument("--source", type=str, default="dooce",
                        help="Corpus identifier (used in entry IDs)")
    parser.add_argument("--output", type=str, default="outputs",
                        help="Directory to save artifacts")
    parser.add_argument("--n-clusters", type=int, default=None,
                        help="Number of clusters for conditions D, E (default: auto-selected via silhouette score)")
    args = parser.parse_args()

    conditions = [args.condition] if args.condition else ALL_CONDITIONS
    run_dirs = []

    for c in conditions:
        run_dir = run_condition(c, args.csv, args.source, args.output, args.n_clusters)
        run_dirs.append(run_dir)

    if len(run_dirs) > 1:
        from pipeline.evaluation.comparator import compare
        comparison_path = Path(args.output) / "comparison.md"
        compare(run_dirs, output_path=comparison_path)
        print(f"\nComparison saved → {comparison_path}")


if __name__ == "__main__":
    main()
