"""
Moduł analizy trendów czasowych oraz dynamiki wzrostów/spadków na rynku nieruchomości.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class TrendAnalysis:
    """Klasa dedykowana wyliczaniu trendów czasowych dodawanych ofert."""

    @staticmethod
    def offers_per_month(df: pd.DataFrame) -> pd.Series:
        """Wylicza wolumen zarejestrowanych ogłoszeń w ujęciu miesięcznym."""
        if df.empty or "date_added" not in df.columns:
            return pd.Series(dtype=int)

        try:
            dates = pd.to_datetime(df["date_added"])
            return df.groupby(dates.dt.to_period("M")).size()
        except Exception as e:
            logger.error(f"Błąd analizy miesięcznej trendu: {e}")
            return pd.Series(dtype=int)

    @staticmethod
    def offers_per_quarter(df: pd.DataFrame) -> pd.Series:
        """Wylicza wolumen zarejestrowanych ogłoszeń w ujęciu kwartalnym."""
        if df.empty or "date_added" not in df.columns:
            return pd.Series(dtype=int)

        try:
            dates = pd.to_datetime(df["date_added"])
            return df.groupby(dates.dt.to_period("Q")).size()
        except Exception as e:
            logger.error(f"Błąd analizy kwartalnej trendu: {e}")
            return pd.Series(dtype=int)

    @staticmethod
    def market_growth_rate(df: pd.DataFrame) -> float:
        """
        Oblicza uproszczoną stopę dynamiki zmian cen na rynku nieruchomości.
        Porównuje średnią cenę z najświeższego miesiąca do miesiąca najstarszego.
        """
        if df.empty or "date_added" not in df.columns or "price_per_m2" not in df.columns:
            return 0.0

        try:
            df_copy = df.copy()
            df_copy["date_period"] = pd.to_datetime(df_copy["date_added"]).dt.to_period("M")
            grouped = df_copy.groupby("date_period")["price_per_m2"].mean().sort_index()

            if len(grouped) < 2:
                return 0.0

            oldest_price = grouped.iloc[0]
            newest_price = grouped.iloc[-1]

            growth_rate = ((newest_price - oldest_price) / oldest_price) * 100
            return float(round(growth_rate, 2))
        except Exception as e:
            logger.error(f"Błąd wyliczania dynamiki wzrostu rynku: {e}")
            return 0.0