"""Optional package-powered visuals for boolean_algebra_pycharm.py."""

from pathlib import Path
import csv


def create_boolean_package_visuals(output_folder: Path):
    """Create polished PNG truth-table charts with pandas and matplotlib."""
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns
    except ImportError:
        print("\nOptional charts skipped. Install them with:")
        print("pip install -r requirements.txt")
        return []

    files = []
    csv_files = sorted(output_folder.glob("*.csv"))
    for csv_path in csv_files:
        frame = pd.read_csv(csv_path)
        numeric = frame.select_dtypes(include="number")
        if numeric.empty:
            continue
        figure_width = max(6, numeric.shape[1] * 1.25)
        figure_height = max(3.5, numeric.shape[0] * 0.55)
        fig, ax = plt.subplots(figsize=(figure_width, figure_height))
        sns.heatmap(numeric, annot=True, fmt="g", cmap=["#f1f5f9", "#86efac"],
                    cbar=False, linewidths=1, linecolor="white", ax=ax)
        ax.set_title(csv_path.stem.replace("_", " ").title(), fontsize=15,
                     color="#173f70", fontweight="bold")
        ax.set_ylabel("Input combination / row")
        fig.tight_layout()
        png_path = output_folder / f"{csv_path.stem}_chart.png"
        fig.savefig(png_path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        files.append(png_path)
    print(f"\nPackage visuals created: {len(files)} PNG charts")
    return files
