"""
Prompt templates for single-choice and multiple-choice questions.
"""


def build_single_choice_prompt(question_data: dict) -> dict:
    """
    Build system and user prompts for single-choice questions.

    Args:
        question_data: Dict containing 'question' and 'choices'.

    Returns:
        Dict with 'system_prompt' and 'user_prompt'.
    """
    options = list(question_data["choices"].keys())
    options_str = ", ".join(options)
    choices_text = "\n".join(
        [f"{k}. {v}" for k, v in question_data["choices"].items()]
    )

    system_prompt = (
        f"You are a professional meteorological evaluation system. "
        f"Strictly follow these rules:\n"
        f"1. Output only the correct option letter ({options_str}).\n"
        f"2. Do not output any other characters, spaces, punctuation, or explanations.\n"
        f"3. If uncertain, randomly select one option from {options_str}."
    )

    user_prompt = (
        f"Please answer the following single-choice question:\n\n"
        f"Question: {question_data['question']}\n"
        f"Choices:\n{choices_text}\n\n"
        f"Strictly output only one uppercase letter from {options_str}, "
        f"in the exact format:\n"
        f"Prediction Answer: 'X'"
    )

    return {"system_prompt": system_prompt, "user_prompt": user_prompt}


def build_multiple_choice_prompt(question_data: dict) -> dict:
    """
    Build system and user prompts for multiple-choice questions.

    Args:
        question_data: Dict containing 'question' and 'choices'.

    Returns:
        Dict with 'system_prompt' and 'user_prompt'.
    """
    options = list(question_data["choices"].keys())
    options_str = ", ".join(options)
    choices_text = "\n".join(
        [f"{k}. {v}" for k, v in question_data["choices"].items()]
    )

    system_prompt = (
        f"You are a professional meteorological evaluation system. "
        f"Strictly follow these rules:\n"
        f"1. Output only the correct option letters ({options_str}).\n"
        f"2. Do not output any other characters, spaces, punctuation, or explanations.\n"
        f"3. If uncertain, randomly select multiple options from {options_str}."
    )

    user_prompt = (
        f"Please answer the following multiple-choice question:\n\n"
        f"Question: {question_data['question']}\n"
        f"Choices:\n{choices_text}\n\n"
        f"Strictly output only the uppercase letter combination from {options_str} "
        f"(e.g., 'A', 'B' or 'A', 'C', 'D'), in the exact format:\n"
        f"Prediction Answer: 'X', 'Y', ..."
    )

    return {"system_prompt": system_prompt, "user_prompt": user_prompt}
