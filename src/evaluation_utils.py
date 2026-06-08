"""
Utility functions for ChineseMet Benchmark evaluation.
"""

import ast
import json
import re
from typing import Any, Iterable, List


def read_json_file(file_path: str):
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON data, or None if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format - {file_path}")
        return None


def normalize_task_type(task_type: str) -> str:
    """
    Normalize dataset task labels to a stable internal value.

    Supports the Chinese labels used by ChineseMet as well as common English
    aliases used in examples and downstream extensions.
    """
    normalized = re.sub(r"[\s_\-]+", "", str(task_type).strip().lower())

    if normalized in {"多项选择题", "多选题", "multiplechoice", "mcq"}:
        return "multiple"
    if normalized in {"单项选择题", "单选题", "singlechoice", "scq"}:
        return "single"

    if "多" in normalized and "选" in normalized:
        return "multiple"
    if "单" in normalized and "选" in normalized:
        return "single"
    if "multiple" in normalized:
        return "multiple"
    if "single" in normalized:
        return "single"

    return "unknown"


def extract_prediction(model_response: str, choices_list: list) -> list:
    """
    Extract predicted option letters from the model response.

    Args:
        model_response: Raw text response from the model.
        choices_list: List of valid option letters, e.g., ['A', 'B', 'C', 'D'].

    Returns:
        List of valid, deduplicated option letters in original order.
    """
    if not model_response:
        return []

    valid_choices_set = {str(choice).upper() for choice in choices_list}
    valid_choices = sorted(valid_choices_set)
    valid_pattern = "|".join(re.escape(choice) for choice in valid_choices)

    answer_marker = re.compile(
        r"(?:prediction\s*answer|predicted\s*answer|answer|预测答案|预测结果|答案)\s*[:：]\s*(.*)",
        flags=re.IGNORECASE,
    )
    answer_segments = [
        match.group(1)
        for line in str(model_response).splitlines()
        if (match := answer_marker.search(line))
    ]
    search_text = " ".join(answer_segments) if answer_segments else str(model_response)

    # Prefer standalone option tokens so words such as "answer" do not add A/E/etc.
    token_pattern = re.compile(rf"(?<![A-Z])({valid_pattern})(?![A-Z])")
    valid_choices = token_pattern.findall(search_text.upper())

    # Also accept compact outputs such as "ACD" when the response contains only
    # option letters after separators and quotes are removed.
    if not valid_choices and all(len(choice) == 1 for choice in valid_choices_set):
        compact = re.sub(r"[^A-Z]", "", search_text.upper())
        if compact and all(letter in valid_choices_set for letter in compact):
            valid_choices = list(compact)

    # Deduplicate while preserving order
    seen = set()
    return [x for x in valid_choices if not (x in seen or seen.add(x))]


def parse_answer_list(value: Any) -> List[str]:
    """
    Safely parse a stored answer/prediction list.

    CSV exports store Python-style lists as strings, for example "['A', 'B']".
    This helper avoids eval() while remaining tolerant of plain text outputs.
    """
    if isinstance(value, (list, tuple, set)):
        parsed: Iterable[Any] = value
    else:
        if value != value:
            return []
        text = "" if value is None else str(value).strip()
        if not text:
            return []

        try:
            literal = ast.literal_eval(text)
        except (SyntaxError, ValueError):
            return extract_prediction(text, list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

        if isinstance(literal, (list, tuple, set)):
            parsed = literal
        else:
            return extract_prediction(str(literal), list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    return [str(item).strip().upper() for item in parsed if str(item).strip()]


def format_time(seconds: float) -> str:
    """Format elapsed seconds into a human-readable string."""
    minutes = int(seconds // 60)
    remaining = seconds % 60
    if minutes > 0:
        return f"{minutes} min {remaining:.2f} sec"
    return f"{remaining:.4f} sec"
