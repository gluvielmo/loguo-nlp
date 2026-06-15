import argparse


def main():
    parser = argparse.ArgumentParser(description="Longitudinal journal analysis pipeline")
    parser.add_argument("--condition", type=int, choices=[1, 2, 3, 4], required=True,
                        help="Which condition to run (1=LLM only, 2=BERTopic, 3=Hierarchical+LLM, 4=Hierarchical+Keywords)")
    parser.add_argument("--csv", type=str, default="data/dooce_2009_2023.csv",
                        help="Path to the corpus CSV file")
    parser.add_argument("--source", type=str, default="dooce",
                        help="Corpus identifier (used in entry IDs)")
    parser.add_argument("--output", type=str, default="outputs",
                        help="Directory to save artifacts")
    parser.add_argument("--n-clusters", type=int, default=20,
                        help="Number of clusters (conditions 3 and 4 only)")
    args = parser.parse_args()

    from pipeline.artifacts.saver import save

    if args.condition == 1:
        from conditions.condition1 import run
        artifacts = run(args.csv, source=args.source)
    elif args.condition == 2:
        from conditions.condition2 import run
        artifacts = run(args.csv, source=args.source)
    elif args.condition == 3:
        from conditions.condition3 import run
        artifacts = run(args.csv, source=args.source, n_clusters=args.n_clusters)
    elif args.condition == 4:
        from conditions.condition4 import run
        artifacts = run(args.csv, source=args.source, n_clusters=args.n_clusters)

    run_dir = save(artifacts, output_dir=args.output)

    print(f"\nCondition {args.condition} complete.")
    print(f"Artifacts: {run_dir / 'artifacts.json'}")
    print(f"Report:    {run_dir / 'report.md'}")


if __name__ == "__main__":
    main()
