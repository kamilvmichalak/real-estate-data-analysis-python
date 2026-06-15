"""
Moduł odpowiedzialny za generowanie wykresów punktowych (rozrzutu).
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def area_vs_price_chart(df: pd.DataFrame) -> Figure:
    """
    Generuje wykres punktowy zależności ceny od powierzchni wraz z linią regresji liniowej.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "area" not in df.columns or "price" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')
        return fig

    try:
        x = df["area"].values
        y = df["price"].values / 1000000

        ax.scatter(x, y, alpha=0.6, color="#9467bd", edgecolor="none", label="Oferty")

        if len(x) > 1:
            m, b = np.polyfit(x, y, 1)
            x_line = np.linspace(min(x), max(x), 100)
            ax.plot(x_line, m * x_line + b, color="#d62728", linestyle="-", linewidth=2,
                    label="Linia trendu (regresja)")

        ax.set_title("Zależność ceny od powierzchni nieruchomości", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Powierzchnia (m²)", fontsize=9)
        ax.set_ylabel("Cena (mln USD)", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(fontsize=8)

        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu area_vs_price_chart: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig
