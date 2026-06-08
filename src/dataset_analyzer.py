"""
Dataset analyzer: count subject distributions in a JSON dataset.
"""

import json
import argparse
from collections import defaultdict
from typing import Dict


def count_subjects(file_path: str) -> Dict[str, int]:
    """
    Count occurrences of each subject in a JSON dataset.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Dict mapping subject names to their counts.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    counts = defaultdict(int)
    for item in data:
        subject = item.get("subject", "Unknown")
        counts[subject] += 1

    return dict(counts)


def main():
    parser = argparse.ArgumentParser(description="Analyze subject distribution in dataset")
    parser.add_argument("--input", required=True, help="Path to JSON dataset")
    args = parser.parse_args()

    counts = count_subjects(args.input)
    total = sum(counts.values())

    print(f"{'Subject':<30} | Count")
    print("-" * 50)
    for subject, count in sorted(counts.items()):
        print(f"{subject:<30} | {count}")
    print("-" * 50)
    print(f"{'Total':<30} | {total}")


if __name__ == "__main__":
    main()
