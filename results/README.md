# Results

This directory contains evaluation outputs from various Large Language Models (LLMs) tested on the ChineseMet benchmark.

## Directory Structure

```text
results/
|-- reports/          # Detailed prediction reports (JSON)
|   |-- {Model}_output.json         # Full predictions for all questions
|   `-- {Model}_error_report.json   # Incorrect predictions only
|-- logs/             # Execution logs from API calls
|   `-- {Model}_result.log          # Raw inference logs
`-- comparisons/      # Prediction vs. ground-truth comparisons
    `-- {Model}_pred_true.csv       # Side-by-side prediction comparison
```

## File Naming Convention

All files follow the pattern: `{ModelName}_{Type}.{Ext}`

- **ModelName**: Standardized model identifier (e.g., `Qwen2.5-72B`, `DeepSeek-R1`, `GLM4-230B`)
- **Type**: `output`, `error_report`, `result`, or `pred_true`
- **Ext**: `json`, `log`, or `csv`

## Models Evaluated

| Model | Reports | Logs | Comparisons |
|-------|---------|------|-------------|
| ChatGLM4-130B | yes | yes | no |
| GLM-130B | no | yes | yes |
| GLM4-230B | yes | yes | yes |
| DeepSeek-R1 | no | yes | yes |
| GPT-OSS-20B | no | yes | no |
| Qwen2.5-72B | yes | yes | no |
| Qwen3 | yes | yes | yes |
| Qwen3-8B | no | yes | no |
| Qwen3-30B-A3B | yes | yes | yes |
| Qwen3-30B-A3B-Think | yes | yes | no |

## Notes

- `_output.json`: Contains the full dataset with an added `model_pred` field for each question.
- `_error_report.json`: Contains only the questions where the model's prediction did not match the ground truth.
- `_result.log`: Raw API interaction logs (may contain internal endpoints; sanitize before sharing).
- `_pred_true.csv`: Two-column CSV (`Pred`, `True`) for easy programmatic analysis.
