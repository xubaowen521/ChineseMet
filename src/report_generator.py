"""
Report generator for ChineseMet Benchmark.
Produces full output JSON and error reports.
"""

import json
import os
from typing import List, Dict, Any


def generate_reports(
    dataset: List[Dict[str, Any]],
    predictions: List[List[str]],
    output_dir: str,
    model_name: str,
) -> None:
    """
    Generate evaluation reports.

    Args:
        dataset: Original dataset items.
        predictions: Model predictions aligned with dataset.
        output_dir: Directory to save report files.
        model_name: Name of the evaluated model.
    """
    os.makedirs(output_dir, exist_ok=True)
    full_output_path = os.path.join(output_dir, f"{model_name}_output.json")
    error_report_path = os.path.join(output_dir, f"{model_name}_error_report.json")

    full_records = []
    error_records = []

    for item, pred in zip(dataset, predictions):
        record = item.copy()
        record["model_pred"] = pred
        full_records.append(record)

        if set(item.get("answer", [])) != set(pred):
            error_records.append({
                "id": item.get("id"),
                "subject": item.get("subject"),
                "question": item.get("question"),
                "correct_answer": item.get("answer"),
                "model_prediction": pred,
            })

    with open(full_output_path, "w", encoding="utf-8") as f:
        json.dump(full_records, f, ensure_ascii=False, indent=2)

    with open(error_report_path, "w", encoding="utf-8") as f:
        json.dump(error_records, f, ensure_ascii=False, indent=2)

    print(f"Full output  : {full_output_path}")
    print(f"Error report : {error_report_path}")
