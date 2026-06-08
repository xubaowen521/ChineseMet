<div align="center">

# ChineseMet Benchmark

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Dataset](https://img.shields.io/badge/Dataset-7K%2B%20Questions-green.svg)]()

**A comprehensive Chinese meteorological benchmark for evaluating Large Language Models.**

[Overview](#overview) • [Dataset](#dataset) • [Quick Start](#quick-start) • [Results](#results) • [Citation](#citation)

</div>

---

## Overview

ChineseMet is a domain-specific benchmark for systematically assessing how well Large Language Models (LLMs) understand Chinese meteorological knowledge. Unlike general-purpose benchmarks, ChineseMet focuses on meteorology-specific concepts, principles, and applied forecasting skills.

### Key Features

- **Domain Coverage**: 20 subject labels across meteorological theory, observation, forecasting, services, and applied meteorology.
- **Question Types**: 5,078 single-choice and 1,979 multiple-choice questions.
- **Automated Evaluation**: A complete evaluation framework supporting OpenAI-compatible APIs for batch model assessment.

---

## Dataset

### Statistics

| Property | Value |
|----------|-------|
| Total Questions | 7,057 |
| Subject Labels | 20 |
| Single-Choice | 5,078 |
| Multiple-Choice | 1,979 |
| Language | Chinese |

### Files

| File | Description | Size |
|------|-------------|------|
| `ChineseMet.json` | Full dataset with answers | ~3.8 MB |

### Data Fields

```json
{
  "id": 0,
  "subject": "天气分析",
  "task": "多项选择题",
  "question": "根据台风本身的云系及其变化可以判别台风的路径，以下说法正确的是：",
  "choices": {
    "A": "台风朝其云区长轴方向移动。",
    "B": "台风向云区稠密的地方移动。",
    "C": "如果台风呈“9”字，台风将向西移。",
    "D": "如果台风呈“6”字，台风将北上转向。"
  },
  "answer": ["A", "B", "C", "D"],
  "analysis": ""
}
```

### Subject Distribution

The dataset covers the following subject labels:

- 天气学原理与方法
- 雷达气象学
- 卫星气象应用
- 动力气象学
- 气候学与古气候学
- 中小尺度天气动力学
- 大气物理学
- 气象专业英语
- 大气环流概论
- 天气分析
- 数值天气预报
- 边界层气象学
- 气象灾害学
- 气象公共服务
- 天气预报基本技能
- 大气探测
- 气象常识
- 天气诊断分析
- 应用气象学
- 气象学基本概念

---

## Quick Start

### Prerequisites

- Python >= 3.8
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/ChineseMet.git
cd ChineseMet

# Install dependencies
pip install -r src/requirements.txt
```

Optional: test your API endpoint before launching the full benchmark.

```bash
cd src
python api_connection_test.py \
    --base_url http://localhost:8000/v1 \
    --api_key YOUR_API_KEY \
    --model your-model-name
```

### Evaluate a Model

```bash
cd src
python run_evaluation.py \
    --model_name your-model-name \
    --dataset_path ../ChineseMet.json \
    --output_dir ./outputs \
    --api_base http://localhost:8000/v1 \
    --api_key YOUR_API_KEY
```

### Analyze Results

**By question type (single-choice vs multiple-choice):**

```bash
python question_type_evaluator.py \
    --csv ./outputs/your-model_pred_true.csv \
    --dataset ../ChineseMet.json
```

**By meteorological subfield:**

```bash
python comparative_analyzer.py \
    --full ../ChineseMet.json \
    --error ./outputs/your-model_error_report.json
```

**Generate visualizations:**

```bash
python -c "
from result_visualizer import plot_heatmap
# See examples/generate_heatmap.py for full example
"
```

### Examples

Check the [`examples/`](examples/) directory for detailed usage examples:

| Example | Description |
|---------|-------------|
| `basic_evaluation.py` | Basic model evaluation pipeline |
| `analyze_by_question_type.py` | Separate metrics for SCQ/MCQ |
| `generate_heatmap.py` | Generate comparison heatmaps |

---

## Results

### Evaluated Models

| Model | Overall Accuracy | Macro-F1 |
|-------|------------------|----------|
| Qwen3-30B-A3B-Think | 69.05% | 78.75% |
| Qwen2.5-72B | 69.04% | 78.55% |
| Qwen3 | 68.70% | 78.32% |
| Qwen3-30B-A3B | 66.22% | 76.44% |
| GLM4-230B | 62.53% | 72.95% |
| ChatGLM4-130B | 60.10% | 71.79% |

These scores are recomputed from the JSON files in [`results/reports/`](results/reports/). Additional CSV comparisons and logs are available in [`results/`](results/).

---

## Project Structure

```text
ChineseMet/
|-- ChineseMet.json                  # Full dataset with answers
|-- src/                             # Evaluation framework source code
|   |-- run_evaluation.py            # Main evaluation entry point
|   |-- inference_engine.py          # Model inference and scoring engine
|   |-- evaluation_utils.py          # I/O and extraction utilities
|   |-- metrics.py                   # Accuracy and Macro-F1 implementations
|   |-- prompts.py                   # Prompt templates for SCQ and MCQ
|   |-- config.py                    # Centralized configuration management
|   |-- report_generator.py          # Output and error report generation
|   |-- result_visualizer.py         # Heatmap and radar chart generation
|   |-- dataset_analyzer.py          # Dataset subject distribution stats
|   |-- comparative_analyzer.py      # Compare full dataset vs. error report
|   |-- question_type_evaluator.py   # Separate SCQ/MCQ metrics + random baseline
|   |-- api_connection_test.py       # API connectivity verification
|   |-- prediction_logger.py         # Human-readable prediction logs
|   |-- requirements.txt             # Python dependencies
|   `-- README.md                    # Framework documentation
|-- results/                         # Model prediction results
|   |-- reports/                     # JSON prediction reports
|   |-- logs/                        # Execution logs
|   `-- comparisons/                 # Prediction vs. ground-truth CSVs
|-- examples/                        # Usage examples
|   |-- basic_evaluation.py
|   |-- analyze_by_question_type.py
|   `-- generate_heatmap.py
|-- LICENSE                          # MIT License
|-- .gitignore                       # Git ignore rules
`-- README.md                        # This file
```

---

## Evaluation Metrics

### Accuracy

Strict-match accuracy: a prediction is considered correct **only if** the predicted option set exactly matches the ground-truth answer set.

```
Accuracy = (# of exactly correct predictions) / (total questions)
```

### Macro-F1

Macro-averaged F1 score computed per-sample and then averaged across the entire dataset. This metric tolerates partial matches on multiple-choice questions.

```
F1_i = 2 * precision_i * recall_i / (precision_i + recall_i)
Macro-F1 = average(F1_i) over all samples
```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- Report bugs or issues
- Add new meteorological questions
- Improve evaluation metrics
- Add support for new models
- Improve documentation

---

## Citation

If you use ChineseMet in your research, please cite:

```bibtex
@misc{chinesemet2025,
  title={ChineseMet: A Comprehensive Chinese Meteorological Evaluation Benchmark for Large Language Models},
  author={Xu, Baowen and Yu, Tingzhao and Gao, Song and Jin, Qizhao},
  year={2025},
  howpublished={\url{https://github.com/your-org/ChineseMet}}
}
```

---

## License

This project is released under the [MIT License](LICENSE). The dataset is provided for academic and research purposes.

## Contact

For questions or contributions, please open an issue in the repository.
