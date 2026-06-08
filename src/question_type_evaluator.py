"""
Question-type evaluator: separate single-choice and multiple-choice metrics.
Also supports random-baseline evaluation.
"""

import argparse
import random
from typing import List

import pandas as pd

from evaluation_utils import parse_answer_list, read_json_file
from metrics import evaluate_score


def _resolve_column(df: pd.DataFrame, candidates: List[str]) -> str:
    """Find a column by trying common names case-insensitively."""
    lookup = {column.lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    raise ValueError(
        f"Expected one of columns {candidates}, but found {list(df.columns)}"
    )


def split_by_question_type(pred_path: str, true_path: str = None):
    """
    Split predictions and truths by question type.

    Args:
        pred_path: Path to pred_true CSV file.
        true_path: Optional path to dataset JSON for type info.

    Returns:
        Tuple of (scq_preds, scq_trues, mcq_preds, mcq_trues).
    """
    df = pd.read_csv(pred_path)
    pred_col = _resolve_column(df, ["Pred", "Prediction", "model_pred"])
    true_col = _resolve_column(df, ["True", "TRUE", "Answer", "GroundTruth"])
    preds = df[pred_col].apply(parse_answer_list).tolist()
    trues = df[true_col].apply(parse_answer_list).tolist()

    scq_preds, scq_trues = [], []
    mcq_preds, mcq_trues = [], []

    for p, t in zip(preds, trues):
        if len(t) == 1:
            scq_preds.append(p)
            scq_trues.append(t)
        else:
            mcq_preds.append(p)
            mcq_trues.append(t)

    return scq_preds, scq_trues, mcq_preds, mcq_trues


def generate_random_predictions(y_true: List[List[str]], num_options: List[int]) -> List[List[str]]:
    """
    Generate random baseline predictions.

    Args:
        y_true: True answer lists.
        num_options: Number of available options per question.

    Returns:
        Random predictions.
    """
    predictions = []
    for true, n in zip(y_true, num_options):
        options = [chr(65 + i) for i in range(n)]
        if len(true) == n:
            predictions.append(sorted(options))
        else:
            sampled = random.sample(options, len(true))
            predictions.append(sorted(sampled))
    return predictions


def main():
    parser = argparse.ArgumentParser(description="Evaluate by question type")
    parser.add_argument("--csv", required=True, help="Path to pred_true CSV")
    parser.add_argument("--dataset", help="Path to dataset JSON (for random baseline)")
    parser.add_argument("--random_baseline", action="store_true", help="Evaluate random baseline")
    args = parser.parse_args()

    scq_preds, scq_trues, mcq_preds, mcq_trues = split_by_question_type(args.csv)

    if args.random_baseline and args.dataset:
        data = read_json_file(args.dataset)
        num_options = [len(item["choices"]) for item in data]
        trues_all = [item["answer"] for item in data]
        random_preds = generate_random_predictions(trues_all, num_options)

        # Re-split random predictions
        rand_scq_preds, rand_scq_trues = [], []
        rand_mcq_preds, rand_mcq_trues = [], []
        for p, t in zip(random_preds, trues_all):
            if len(t) == 1:
                rand_scq_preds.append(p)
                rand_scq_trues.append(t)
            else:
                rand_mcq_preds.append(p)
                rand_mcq_trues.append(t)

        print("=" * 50)
        print("Random Baseline Results")
        print("=" * 50)
        mcq_rand = evaluate_score(rand_mcq_trues, rand_mcq_preds)
        scq_rand = evaluate_score(rand_scq_trues, rand_scq_preds)
        print(f"Multiple-choice | Acc: {mcq_rand['Accuracy (%)']} % | F1: {mcq_rand['Macro-F1 (%)']} %")
        print(f"Single-choice   | Acc: {scq_rand['Accuracy (%)']} % | F1: {scq_rand['Macro-F1 (%)']} %")
        print("=" * 50)

    print("\nModel Results")
    print("=" * 50)
    mcq_scores = evaluate_score(mcq_trues, mcq_preds)
    scq_scores = evaluate_score(scq_trues, scq_preds)
    print(f"Multiple-choice | Acc: {mcq_scores['Accuracy (%)']} % | F1: {mcq_scores['Macro-F1 (%)']} %")
    print(f"Single-choice   | Acc: {scq_scores['Accuracy (%)']} % | F1: {scq_scores['Macro-F1 (%)']} %")


if __name__ == "__main__":
    main()
