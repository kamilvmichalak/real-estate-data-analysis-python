"""
Moduł analizujący atrakcyjność rynkową poszczególnych lokalizacji (miast i dzielnic).
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class LocationAnalysis:
    """Analityka przestrzenna i lokalizacyjna."""

    @staticmethod
    def cheapest_locations(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
        """Zwraca najtańsze lokalizacje pod kątem średniej ceny za metr kwadratowy."""
        if df.empty or "district" not in df.columns or "price_per_m2" not in df.columns:
            return pd.DataFrame()
        grouped = df.groupby(["city", "district"])["price_per_m2"].mean().reset_index()
        return grouped.sort_values(by="price_per_m2", ascending=True).head(limit)

    @staticmethod
    def most_expensive_locations(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
        """Zwraca najdroższe lokalizacje pod kątem średniej ceny za metr kwadratowy."""
        if df.empty or "district" not in df.columns or "price_per_m2" not in df.columns:
            return pd.DataFrame()
        grouped = df.groupby(["city", "district"])["price_per_m2"].mean().reset_index()
        return grouped.sort_values(by="price_per_m2", ascending=False).head(limit)

    @staticmethod
    def compare_locations(df: pd.DataFrame, city_a: str, city_b: str) -> pd.DataFrame:
        """Porównuje podstawowe metryki statystyczne dla dwóch wybranych miast."""
        if df.empty:
            return pd.DataFrame()
        filtered = df[df["city"].str.lower().isin([city_a.lower(), city_b.lower()])]
        if filtered.empty:
            return pd.DataFrame()

        metrics = filtered.groupby("city").agg({
            "price": ["mean", "median"],
            "price_per_m2": ["mean"],
            "area": ["mean"]
        }).round(2)
        return metrics