"""
Inference engine for ChineseMet Benchmark.
Handles model API calls, prediction extraction, and metric computation.
"""

import logging
import os
import time
from typing import List

import pandas as pd
from openai import OpenAI

from config import ModelConfig, EvaluationConfig
from evaluation_utils import extract_prediction, normalize_task_type, read_json_file
from metrics import evaluate_score
from prompts import build_single_choice_prompt, build_multiple_choice_prompt
from report_generator import generate_reports


def create_openai_client(config: ModelConfig) -> OpenAI:
    """Create an OpenAI-compatible client from configuration."""
    return OpenAI(base_url=config.base_url, api_key=config.api_key)


def run_evaluation(config: EvaluationConfig, model_config: ModelConfig) -> None:
    """
    Run the full evaluation pipeline.

    Args:
        config: Evaluation configuration.
        model_config: Model API configuration.
    """
    client = create_openai_client(model_config)
    log_path = os.path.join(config.output_dir, f"{model_config.model_name}_result.log")
    logging.basicConfig(
        filename=log_path,
        level=getattr(logging, config.log_level),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    dataset = read_json_file(config.dataset_path)
    if dataset is None:
        raise RuntimeError(f"Failed to load dataset from {config.dataset_path}")

    y_true: List[List[str]] = []
    y_pred: List[List[str]] = []

    for idx, item in enumerate(dataset):
        start_t = time.time()
        task_type = normalize_task_type(item.get("task", ""))
        choices_keys = list(item["choices"].keys())

        if task_type == "multiple":
            prompt = build_multiple_choice_prompt(item)
        elif task_type == "single":
            prompt = build_single_choice_prompt(item)
        else:
            logging.warning(
                "Unknown task type '%s' for item %s; inferring from answer length",
                item.get("task", ""),
                idx,
            )
            if len(item.get("answer", [])) > 1:
                prompt = build_multiple_choice_prompt(item)
            else:
                prompt = build_single_choice_prompt(item)

        try:
            response = client.chat.completions.create(
                model=model_config.model_name,
                messages=[
                    {"role": "system", "content": prompt["system_prompt"]},
                    {"role": "user", "content": prompt["user_prompt"]},
                ],
                temperature=model_config.temperature,
                max_tokens=model_config.max_tokens,
            )
            model_response = response.choices[0].message.content
        except Exception as e:
            logging.error(f"API call failed for item {idx}: {e}")
            model_response = ""

        pred = extract_prediction(model_response, choices_keys)
        print(f"[{idx}] Pred: {pred} | True: {item['answer']} | Time: {time.time()-start_t:.2f}s")

        y_pred.append(pred)
        y_true.append(item["answer"])

    scores = evaluate_score(y_true, y_pred)
    print(f"\nEvaluation Results for {model_config.model_name}:")
    print(f"  Accuracy  : {scores['Accuracy (%)']} %")
    print(f"  Macro-F1  : {scores['Macro-F1 (%)']} %")
    logging.info(f"Accuracy (%): {scores['Accuracy (%)']}")
    logging.info(f"Macro-F1 (%): {scores['Macro-F1 (%)']}")

    generate_reports(
        dataset=dataset,
        predictions=y_pred,
        output_dir=config.output_dir,
        model_name=model_config.model_name,
    )

    # Save prediction-true comparison as CSV
    csv_path = os.path.join(config.output_dir, f"{model_config.model_name}_pred_true.csv")
    pd.DataFrame({"Pred": y_pred, "True": y_true}).to_csv(csv_path, index=False)
    print(f"Results saved to {config.output_dir}")
