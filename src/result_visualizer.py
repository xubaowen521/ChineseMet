"""
Result visualizer for ChineseMet Benchmark.
Generates heatmaps and radar charts from evaluation results.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_heatmap(
    accuracy_data: list,
    row_labels: list,
    col_labels: list,
    output_path: str = "heatmap.pdf",
    cmap: str = "Blues",
    figsize: tuple = (14, 12),
) -> None:
    """
    Plot a heatmap of model accuracies across meteorological subfields.

    Args:
        accuracy_data: 2D list of accuracy percentages.
        row_labels: List of subfield names (y-axis).
        col_labels: List of model names (x-axis).
        output_path: Path to save the figure.
        cmap: Colormap name.
        figsize: Figure size in inches.
    """
    df = pd.DataFrame(data=accuracy_data, index=row_labels, columns=col_labels)

    plt.figure(figsize=figsize)
    ax = sns.heatmap(
        df,
        cmap=cmap,
        annot=True,
        fmt=".2f",
        cbar=True,
        yticklabels=True,
        xticklabels=True,
        cbar_kws={"label": "Accuracy (%)"},
    )

    ax.set_xlabel("Models", fontsize=12)
    ax.set_ylabel("Meteorological Subfields", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Heatmap saved to {output_path}")


def plot_radar(
    model_data: dict,
    categories: list,
    output_path: str = "radar_chart.pdf",
    figsize: tuple = (12, 10),
) -> None:
    """
    Plot a radar chart for multi-model comparison.

    Args:
        model_data: Dict mapping model names to lists of accuracy values (0-1).
        categories: List of dimension labels.
        output_path: Path to save the figure.
        figsize: Figure size in inches.
    """
    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    colors = [
        "#4287f5", "#f5a623", "#f54242",
        "#42f5a1", "#a642f5", "#f5f542",
    ]

    for i, (model_name, values) in enumerate(model_data.items()):
        values_closed = values + [values[0]]
        ax.plot(angles, values_closed, color=colors[i % len(colors)],
                linewidth=2, label=model_name)
        ax.fill(angles, values_closed, color=colors[i % len(colors)], alpha=0.15)

    ax.set_thetagrids(np.degrees(angles[:-1]), categories, rotation=0, fontsize=8)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.linspace(0, 1.0, 5))
    ax.set_yticklabels([f"{int(x*100)}%" for x in np.linspace(0, 1.0, 5)])
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1), fontsize=9)

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Radar chart saved to {output_path}")
