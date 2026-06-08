"""
Comparative analyzer: compare subject distributions between two datasets.
Typically used to compare the full dataset against an error report.
"""

import json
import argparse
from collections import defaultdict
from typing import Dict


def count_subjects(file_path: str) -> Dict[str, int]:
    """Count subject occurrences in a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    counts = defaultdict(int)
    for item in data:
        subject = item.get("subject", "Unknown")
        counts[subject] += 1
    return dict(counts)


def compare_distributions(full_counts: Dict[str, int], error_counts: Dict[str, int]) -> Dict:
    """
    Compare two distributions and compute per-subject accuracy.

    Args:
        full_counts: Subject counts from the full dataset.
        error_counts: Subject counts from the error report.

    Returns:
        Dict with per-subject statistics.
    """
    all_subjects = set(full_counts.keys()).union(error_counts.keys())
    results = {}
    for subject in all_subjects:
        total = full_counts.get(subject, 0)
        errors = error_counts.get(subject, 0)
        correct = total - errors
        accuracy = (correct / total * 100) if total > 0 else 0.0
        results[subject] = {
            "total": total,
            "errors": errors,
            "correct": correct,
            "accuracy (%)": accuracy,
        }
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Compare dataset distribution with error report"
    )
    parser.add_argument("--full", required=True, help="Path to full dataset JSON")
    parser.add_argument("--error", required=True, help="Path to error report JSON")
    args = parser.parse_args()

    full_counts = count_subjects(args.full)
    error_counts = count_subjects(args.error)
    metrics = compare_distributions(full_counts, error_counts)

    print(f"{'Subject':<30} | Accuracy (%)")
    print("-" * 60)
    for subject, stats in sorted(metrics.items()):
        print(f"{subject:<30} | {stats['accuracy (%)']:.2f}")

    total_full = sum(full_counts.values())
    total_errors = sum(error_counts.values())
    overall = (total_full - total_errors) / total_full * 100 if total_full > 0 else 0.0
    print("-" * 60)
    print(f"{'Overall':<30} | {overall:.2f}")


if __name__ == "__main__":
    main()
