#!/usr/bin/env python3
"""
Example: Basic model evaluation on ChineseMet.

This script demonstrates the simplest way to evaluate a model
using the ChineseMet benchmark framework.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import EvaluationConfig, ModelConfig
from inference_engine import run_evaluation


def main():
    # Configure evaluation
    eval_config = EvaluationConfig(
        dataset_path="../ChineseMet.json",
        output_dir="./outputs",
    )

    # Configure model API
    model_config = ModelConfig(
        base_url="http://localhost:8000/v1",
        api_key="EMPTY",
        model_name="your-model-name",
        temperature=0.4,
    )

    # Run evaluation
    run_evaluation(eval_config, model_config)


if __name__ == "__main__":
    main()
