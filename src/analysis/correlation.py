"""
Moduł statystyczny wyliczający współczynniki korelacji pomiędzy cechami ilościowymi nieruchomości.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class CorrelationAnalysis:
    """Klasa realizująca matematyczną analizę korelacji cech stałych."""

    @staticmethod
    def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
        """
        Oblicza macierz korelacji Pearsona dla zmiennych ilościowych:
        price, area, rooms, floor, year_built.

        Returns:
            pd.DataFrame: Macierz współczynników korelacji.
        """
        target_columns = ["price", "area", "rooms", "floor", "year_built"]

        # Odfiltrowanie kolumn, które faktycznie występują w przesłanym zbiorze danych
        available_cols = [col for col in target_columns if col in df.columns]

        if len(available_cols) < 2:
            logger.warning("Niewystarczająca liczba zmiennych numerycznych do wyznaczenia korelacji.")
            return pd.DataFrame()

        try:
            # Rzutowanie na typ numeryczny dla zapewnienia stabilności obliczeń numpy/pandas
            numeric_df = df[available_cols].apply(pd.to_numeric, errors="coerce")
            correlation_matrix = numeric_df.corr(method="pearson").round(4)
            return correlation_matrix
        except Exception as e:
            logger.error(f"Błąd obliczania macierzy korelacji: {e}")
            return pd.DataFrame()