#!/usr/bin/env python3
"""
Example: Analyze evaluation results by question type.

This script shows how to separate single-choice and multiple-choice
questions and compute metrics for each type.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from evaluation_utils import parse_answer_list, read_json_file
from metrics import evaluate_score
import pandas as pd


def _resolve_column(df: pd.DataFrame, candidates: list[str]) -> str:
    """Find a column by trying common names case-insensitively."""
    lookup = {column.lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    raise ValueError(
        f"Expected one of columns {candidates}, but found {list(df.columns)}"
    )


def analyze_by_question_type(csv_path: str, dataset_path: str):
    """Analyze results separately for single-choice and multiple-choice questions."""
    df = pd.read_csv(csv_path)
    dataset = read_json_file(dataset_path)
    pred_col = _resolve_column(df, ["Pred", "Prediction", "model_pred"])
    true_col = _resolve_column(df, ["True", "TRUE", "Answer", "GroundTruth"])

    scq_preds, scq_trues = [], []
    mcq_preds, mcq_trues = [], []

    for i, row in df.iterrows():
        pred = parse_answer_list(row[pred_col])
        true = parse_answer_list(row[true_col])

        if len(true) == 1:
            scq_preds.append(pred)
            scq_trues.append(true)
        else:
            mcq_preds.append(pred)
            mcq_trues.append(true)

    print("Single-Choice Questions:")
    scq_scores = evaluate_score(scq_trues, scq_preds)
    print(f"  Accuracy:  {scq_scores['Accuracy (%)']} %")
    print(f"  Macro-F1:  {scq_scores['Macro-F1 (%)']} %")

    print("\nMultiple-Choice Questions:")
    mcq_scores = evaluate_score(mcq_trues, mcq_preds)
    print(f"  Accuracy:  {mcq_scores['Accuracy (%)']} %")
    print(f"  Macro-F1:  {mcq_scores['Macro-F1 (%)']} %")


if __name__ == "__main__":
    analyze_by_question_type(
        csv_path="../results/comparisons/your-model_pred_true.csv",
        dataset_path="../ChineseMet.json",
    )
