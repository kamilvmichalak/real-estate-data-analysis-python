"""
Moduł realizujący analizy statystyczne wskaźników cenowych na rynku nieruchomości.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class PriceAnalysis:
    """Analityka statystyczna oparta na cenach nieruchomości."""

    @staticmethod
    def average_price_by_city(df: pd.DataFrame) -> pd.Series:
        """Oblicza średnią cenę nieruchomości w poszczególnych miastach."""
        if df.empty or "city" not in df.columns or "price" not in df.columns:
            return pd.Series(dtype=float)
        return df.groupby("city")["price"].mean().round(2)

    @staticmethod
    def median_price_by_city(df: pd.DataFrame) -> pd.Series:
        """Oblicza medianę ceny nieruchomości w podziale na miasta."""
        if df.empty or "city" not in df.columns or "price" not in df.columns:
            return pd.Series(dtype=float)
        return df.groupby("city")["price"].median().round(2)

    @staticmethod
    def average_price_by_property_type(df: pd.DataFrame) -> pd.Series:
        """Zwraca średnią cenę ze względu na rodzaj posiadłości."""
        if df.empty or "property_type" not in df.columns or "price" not in df.columns:
            return pd.Series(dtype=float)
        return df.groupby("property_type")["price"].mean().round(2)

    @staticmethod
    def average_price_per_square_meter(df: pd.DataFrame) -> pd.Series:
        """Oblicza średnią cenę za metr kwadratowy powierzchni użytkowej w miastach."""
        if df.empty or "city" not in df.columns or "price_per_m2" not in df.columns:
            return pd.Series(dtype=float)
        return df.groupby("city")["price_per_m2"].mean().round(2)