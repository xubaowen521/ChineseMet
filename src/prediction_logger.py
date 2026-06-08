"""
Prediction logger: generate human-readable prediction comparison logs.
"""

import argparse
import os
from typing import List, Dict, Any


def generate_prediction_log(
    dataset: List[Dict[str, Any]],
    predictions: List[List[str]],
    output_path: str,
) -> None:
    """
    Generate a plain-text log comparing predictions with ground truth.

    Args:
        dataset: Original dataset items.
        predictions: Model predictions aligned with dataset.
        output_path: Path to save the log file.
    """
    lines = []
    for item, pred in zip(dataset, predictions):
        qid = item.get("id", "N/A")
        true = item.get("answer", [])
        lines.append(f"{qid} {pred} {true}")
        lines.append("-" * 100)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Prediction log saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate prediction comparison log")
    parser.add_argument("--dataset", required=True, help="Path to dataset JSON")
    parser.add_argument("--predictions", required=True, help="Path to predictions JSON")
    parser.add_argument("--output", default="prediction_comparison.log", help="Output log path")
    args = parser.parse_args()

    import json
    with open(args.dataset, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open(args.predictions, "r", encoding="utf-8") as f:
        predictions = json.load(f)

    generate_prediction_log(dataset, predictions, args.output)


if __name__ == "__main__":
    main()
