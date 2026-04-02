import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import io
from PIL import Image

# Use non-interactive backend
matplotlib.use('Agg')


def generate_dashboard(results):
    """
    Takes a list of result dictionaries and generates
    a dashboard with two charts.
    Returns a PIL Image object that Streamlit can display.
    """
    df = pd.DataFrame(results)

    # Create figure with two side by side charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('#fafafa')

    # --- Chart 1: Quality scores by prompt style ---
    styles = df["style"].tolist()
    x = np.arange(len(styles))
    width = 0.25

    bars1 = ax1.bar(x - width, df["completeness"],
                    width, label="Completeness",
                    color="#6C63FF", alpha=0.85)
    bars2 = ax1.bar(x, df["conciseness"],
                    width, label="Conciseness",
                    color="#48CAE4", alpha=0.85)
    bars3 = ax1.bar(x + width, df["clarity"],
                    width, label="Clarity",
                    color="#95D5B2", alpha=0.85)

    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [s.replace("_", " ").title() for s in styles],
        fontsize=10
    )
    ax1.set_ylabel("Score (1–5)", fontsize=11)
    ax1.set_title("Quality Scores by Prompt Style",
                  fontsize=13, fontweight='bold', pad=15)
    ax1.set_ylim(0, 5.5)
    ax1.legend(fontsize=9)
    ax1.set_facecolor('#f5f5f5')
    ax1.grid(axis='y', alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Add value labels on top of each bar
    for bar in [bars1, bars2, bars3]:
        for rect in bar:
            height = rect.get_height()
            if height > 0:
                ax1.text(
                    rect.get_x() + rect.get_width() / 2.,
                    height + 0.05,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9
                )

    # --- Chart 2: Summary length by prompt style ---
    colors = ["#6C63FF", "#48CAE4", "#95D5B2"]
    bars = ax2.bar(styles, df["summary_length"],
                   color=colors, alpha=0.85)

    ax2.set_xticklabels(
        [s.replace("_", " ").title() for s in styles],
        fontsize=10
    )
    ax2.set_ylabel("Characters", fontsize=11)
    ax2.set_title("Summary Length by Prompt Style",
                  fontsize=13, fontweight='bold', pad=15)
    ax2.set_facecolor('#f5f5f5')
    ax2.grid(axis='y', alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Add value labels on top
    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.,
            height + 10,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=9
        )

    plt.tight_layout(pad=3.0)

    # Convert to PIL Image for Streamlit
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150,
                bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return Image.open(buf)