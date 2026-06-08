# Source Code

This directory contains the evaluation framework source code for the ChineseMet benchmark.

For full documentation, usage examples, and getting started guide, please refer to the [main README](../README.md) in the project root.

## Module Overview

| Module | Purpose |
|--------|---------|
| `run_evaluation.py` | CLI entry point |
| `inference_engine.py` | Model inference and scoring |
| `evaluation_utils.py` | I/O and extraction utilities |
| `metrics.py` | Accuracy and Macro-F1 |
| `prompts.py` | Prompt templates |
| `config.py` | Configuration management |
| `report_generator.py` | Result report generation |
| `result_visualizer.py` | Heatmap and radar charts |
| `dataset_analyzer.py` | Dataset statistics |
| `comparative_analyzer.py` | Compare distributions |
| `question_type_evaluator.py` | SCQ/MCQ evaluation |
| `api_connection_test.py` | API connectivity test |
| `prediction_logger.py` | Prediction logging |
