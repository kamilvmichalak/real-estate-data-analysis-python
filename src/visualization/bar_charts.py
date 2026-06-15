"""
Moduł odpowiedzialny za generowanie wykresów słupkowych.
"""

import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def average_price_by_city_chart(df: pd.DataFrame) -> Figure:
    """
    Generuje wykres słupkowy przedstawiający średnią cenę nieruchomości w lokalizacjach.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "city" not in df.columns or "price" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')
        return fig

    try:
        data = df.groupby("city")["price"].mean().sort_values(ascending=False) / 1000
        bars = ax.bar(data.index, data.values, color="#1f77b4", edgecolor="black", alpha=0.8)

        ax.set_title("Średnia cena nieruchomości według lokalizacji", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Lokalizacja", fontsize=9)
        ax.set_ylabel("Średnia cena (tys. USD)", fontsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=15, labelsize=9)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + (max(data.values) * 0.01), f"{int(yval)}k", ha='center',
                    va='bottom', fontsize=8)

        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu average_price_by_city_chart: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig


def offers_per_type_chart(df: pd.DataFrame) -> Figure:
    """
    Generuje poziomy wykres słupkowy liczby ofert ze względu na typ nieruchomości.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "property_type" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')
        return fig

    try:
        data = df["property_type"].value_counts()
        bars = ax.barh(data.index, data.values, color="#2ca02c", edgecolor="black", alpha=0.8)

        ax.set_title("Liczba dostępnych ofert według typu", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Liczba ogłoszeń", fontsize=9)
        ax.set_ylabel("Typ nieruchomości", fontsize=9)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        for bar in bars:
            xval = bar.get_width()
            ax.text(xval + (max(data.values) * 0.01), bar.get_y() + bar.get_height() / 2.0, f"{int(xval)}", ha='left',
                    va='center', fontsize=8)

        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu offers_per_type_chart: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig
