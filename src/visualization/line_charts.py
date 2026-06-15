"""
Moduł odpowiedzialny za generowanie wykresów liniowych trendów czasowych.
"""

import logging
import pandas as pd
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def offers_trend_chart(df: pd.DataFrame) -> Figure:
    """
    Generuje wykres liniowy przedstawiający dynamikę napływu ofert w czasie.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    if df.empty or "date_added" not in df.columns:
        ax.text(0.5, 0.5, "Brak danych o datach dodania ofert", ha='center', va='center')
        return fig

    try:
        df_copy = df.copy()
        df_copy["date_parsed"] = pd.to_datetime(df_copy["date_added"])
        # Grupowanie dzienne lub miesięczne w zależności od horyzontu danych
        trend = df_copy.groupby(df_copy["date_parsed"].dt.date).size()

        ax.plot(trend.index, trend.values, marker='o', linestyle='-', color="#bcbd22", linewidth=2, markersize=4)

        ax.set_title("Trend napływu ogłoszeń nieruchomości", fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Data rejestracji", fontsize=9)
        ax.set_ylabel("Liczba nowych ofert", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.5)

        fig.autofmt_xdate(rotation=25)
        fig.tight_layout()
    except Exception as e:
        logger.error(f"Błąd generowania wykresu offers_trend_chart: {e}")
        ax.text(0.5, 0.5, "Błąd generowania wykresu", ha='center', va='center')

    return fig