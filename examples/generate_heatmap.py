#!/usr/bin/env python3
"""
Example: Generate visualization heatmap from evaluation results.

This script demonstrates how to create a heatmap comparing
multiple models across meteorological subfields.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from result_visualizer import plot_heatmap


def main():
    # Example data: 5 subfields x 3 models
    accuracy_data = [
        [65.53, 60.61, 51.89],  # Weather Analysis
        [69.16, 59.34, 55.41],  # Satellite Meteorology
        [66.45, 59.26, 55.56],  # Radar Meteorology
        [75.61, 70.49, 71.52],  # Climatology
        [69.34, 62.53, 55.96],  # Mesoscale Meteorology
    ]

    row_labels = [
        "Weather Analysis",
        "Satellite Meteorology",
        "Radar Meteorology",
        "Climatology",
        "Mesoscale Meteorology",
    ]

    col_labels = ["Qwen2.5-72B", "GLM4-230B", "GLM-130B"]

    plot_heatmap(
        accuracy_data=accuracy_data,
        row_labels=row_labels,
        col_labels=col_labels,
        output_path="model_comparison_heatmap.pdf",
    )


if __name__ == "__main__":
    main()
