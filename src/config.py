"""
Configuration module for ChineseMet Benchmark.
Centralizes all configurable parameters to avoid hard-coding.
"""

import os
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for model API connection."""
    base_url: str = "http://localhost:8000/v1"
    api_key: str = "EMPTY"
    model_name: str = "your-model-name"
    temperature: float = 0.4
    max_tokens: int = 10240


@dataclass
class EvaluationConfig:
    """Configuration for evaluation pipeline."""
    dataset_path: str = "../ChineseMet.json"
    output_dir: str = "./outputs"
    log_level: str = "INFO"
    
    def __post_init__(self):
        os.makedirs(self.output_dir, exist_ok=True)
