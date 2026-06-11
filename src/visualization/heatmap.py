"""
Moduł odpowiedzialny za generowanie map ciepła korelacji.
"""

import logging
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def correlation_heatmap(df: pd.DataFrame) -> Figure:
    """
    Generuje mapę ciepła korelacji cech ilościowych z wykorzystaniem seaborn.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    target_columns = ["price", "area", "rooms", "floor", "year_built"]
    available_cols = [col for col in target_columns if col in df.columns]

    if len(available_cols) < 2:
        ax.text(0.5, 0.5, "Zbyt mało zmiennych numerycznych", ha='center', va='center')
        return fig

    try:
        numeric_df = df[available_cols].apply(pd.to_numeric, errors="coerce")
        corr_matrix = numeric_df.corr(method="pearson")

        # Wykorzystanie seaborn do narysowania mapy na osiach matplotlib.Figure
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="CoolTicks" if hasattr(sns, "CoolTicks") else "coolwarm",
            fmt=".2f",
            linewidths=0.5,
            ax=ax,
            vmin=-1,
            vmax=1,
            cbar_kws={'label': 'Współczynnik Pearsona'}
        )

        ax.set_title("Macierz korelacji cech nieruchomości", fontsize=11, fontweight="bold", pad=10)
        ax.tick_params(axis='both', labelsize=9)
        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu correlation_heatmap: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig