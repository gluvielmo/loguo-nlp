import argparse
from pathlib import Path


def run_condition(condition: int, csv: str, source: str, output: str, n_clusters: int) -> Path:
    from pipeline.artifacts.saver import save

    if condition == 1:
        from conditions.condition1 import run
        artifacts = run(csv, source=source)
    elif condition == 2:
        from conditions.condition2 import run
        artifacts = run(csv, source=source)
    elif condition == 3:
        from conditions.condition3 import run
        artifacts = run(csv, source=source, n_clusters=n_clusters)
    elif condition == 4:
        from conditions.condition4 import run
        artifacts = run(csv, source=source, n_clusters=n_clusters)

    run_dir = save(artifacts, output_dir=output)
    print(f"Condition {condition} complete → {run_dir}")
    return run_dir


def main():
    parser = argparse.ArgumentParser(description="Longitudinal journal analysis pipeline")
    parser.add_argument("--condition", type=int, choices=[1, 2, 3, 4],
                        help="Which condition to run. Omit to run all 4.")
    parser.add_argument("--csv", type=str, default="data/dooce_2009_2023.csv",
                        help="Path to the corpus CSV file")
    parser.add_argument("--source", type=str, default="dooce",
                        help="Corpus identifier (used in entry IDs)")
    parser.add_argument("--output", type=str, default="outputs",
                        help="Directory to save artifacts")
    parser.add_argument("--n-clusters", type=int, default=20,
                        help="Number of clusters (conditions 3 and 4 only)")
    args = parser.parse_args()

    conditions = [args.condition] if args.condition else [1, 2, 3, 4]
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
