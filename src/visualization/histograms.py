"""
Moduł odpowiedzialny za analizę rozkładów statystycznych (histogramy i wykresy pudełkowe).
"""

import logging
import pandas as pd
import numpy as np
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def price_distribution_histogram(df: pd.DataFrame) -> Figure:
    """
    Generuje histogram rozkładu cen nieruchomości.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "price" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')
        return fig

    try:
        prices_k = df["price"] / 1000
        bins = min(30, max(10, len(prices_k) // 10))

        ax.hist(prices_k, bins=bins, color="#17becf", edgecolor="black", alpha=0.7, density=False)
        ax.set_title("Rozkład cen nieruchomości na rynku", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Cena (tys. USD)", fontsize=9)
        ax.set_ylabel("Częstość (liczba ofert)", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.5)

        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu price_distribution_histogram: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig


def price_boxplot(df: pd.DataFrame) -> Figure:
    """
    Generuje wykres pudełkowy cen nieruchomości w podziale na główne lokalizacje.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "city" not in df.columns or "price" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')
        return fig

    try:
        top_cities = df["city"].value_counts().head(5).index.tolist()

        plot_data = []
        labels = []
        for city in top_cities:
            city_prices = (df[df["city"] == city]["price"] / 1000).values
            plot_data.append(city_prices)
            labels.append(city)

        if not plot_data:
            ax.text(0.5, 0.5, "Brak danych dla głównych lokalizacji", ha='center', va='center')
            return fig

        ax.boxplot(plot_data, labels=labels, patch_artist=True,
                   boxprops=dict(facecolor="#ff7f0e", color="black", alpha=0.7),
                   medianprops=dict(color="red", linewidth=1.5))

        ax.set_title("Wykres pudełkowy cen (Wychwytywanie outlierów)", fontsize=11, fontweight="bold", pad=10)
        ax.set_ylabel("Cena (tys. USD)", fontsize=9)
        ax.set_xlabel("Lokalizacja", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.tick_params(axis='x', rotation=15, labelsize=9)

        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu price_boxplot: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig
