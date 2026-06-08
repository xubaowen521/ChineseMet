"""
Evaluation metrics for ChineseMet Benchmark.
"""


def calculate_accuracy(y_true: list, y_pred: list) -> float:
    """
    Calculate strict-match accuracy.
    A prediction is correct only if the predicted set exactly matches the true set.

    Args:
        y_true: List of true answer lists, e.g., [['A', 'B'], ['C']]
        y_pred: List of predicted answer lists.

    Returns:
        Accuracy score in the range [0, 1].
    """
    if not y_true:
        return 0.0
    correct = sum(
        1 for true, pred in zip(y_true, y_pred) if set(true) == set(pred)
    )
    return correct / len(y_true)


def calculate_macro_f1(y_true: list, y_pred: list) -> float:
    """
    Calculate macro-averaged F1 score.
    Computes F1 for each sample and averages them.

    Args:
        y_true: List of true answer lists.
        y_pred: List of predicted answer lists.

    Returns:
        Macro-F1 score in the range [0, 1].
    """
    if not y_true:
        return 0.0

    def _f1(true: list, pred: list) -> float:
        true_set, pred_set = set(true), set(pred)
        tp = len(true_set & pred_set)
        fp = len(pred_set - true_set)
        fn = len(true_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    f1_scores = [_f1(true, pred) for true, pred in zip(y_true, y_pred)]
    return sum(f1_scores) / len(f1_scores)


def evaluate_score(y_true: list, y_pred: list) -> dict:
    """
    Compute Accuracy and Macro-F1 in percentage form.

    Args:
        y_true: List of true answer lists.
        y_pred: List of predicted answer lists.

    Returns:
        Dict with 'Accuracy (%)' and 'Macro-F1 (%)'.
    """
    acc = calculate_accuracy(y_true, y_pred)
    macro_f1 = calculate_macro_f1(y_true, y_pred)
    return {
        "Accuracy (%)": round(acc * 100, 2),
        "Macro-F1 (%)": round(macro_f1 * 100, 2),
    }
