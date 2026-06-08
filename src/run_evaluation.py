"""
Main entry point for ChineseMet Benchmark evaluation.
"""

import argparse
import time

from config import EvaluationConfig, ModelConfig
from evaluation_utils import format_time
from inference_engine import run_evaluation


def parse_args():
    parser = argparse.ArgumentParser(
        description="ChineseMet Benchmark: Evaluate LLMs on Chinese meteorological knowledge."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="qwen3_30B_A3B",
        help="Name of the model to evaluate",
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        default="../ChineseMet.json",
        help="Path to the ChineseMet dataset",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./outputs",
        help="Directory to save evaluation outputs",
    )
    parser.add_argument(
        "--api_base",
        type=str,
        default="http://localhost:8000/v1",
        help="Base URL for the model API",
    )
    parser.add_argument(
        "--api_key",
        type=str,
        default="EMPTY",
        help="API key for authentication",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.4,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=10240,
        help="Maximum tokens per response",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    eval_config = EvaluationConfig(
        dataset_path=args.dataset_path,
        output_dir=args.output_dir,
    )
    model_config = ModelConfig(
        base_url=args.api_base,
        api_key=args.api_key,
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    start = time.perf_counter()
    run_evaluation(eval_config, model_config)
    elapsed = time.perf_counter() - start
    print(f"\nTotal execution time: {format_time(elapsed)}")


if __name__ == "__main__":
    main()
