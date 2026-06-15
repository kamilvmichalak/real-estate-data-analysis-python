"""
Moduł odpowiedzialny za czyszczenie, walidację i standaryzację surowych danych rynkowych.
Zapewnia spójność typów danych przed przekazaniem ich do warstwy analitycznej.
"""

import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Klasa realizująca proces ETL (Extract-Transform-Load) w zakresie czyszczenia danych.
    Usuwa duplikaty, uzupełnia braki kadrowe oraz rzutuje typy na numeryczne.
    """

    def __init__(self) -> None:
        self.required_columns = [
            "title", "city", "district", "property_type",
            "area", "rooms", "floor", "year_built", "price", "date_added"
        ]

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Usuwa zduplikowane wiersze z obiektu DataFrame."""
        initial_count = len(df)
        df = df.drop_duplicates()
        final_count = len(df)
        if initial_count - final_count > 0:
            logger.info(f"Usunięto {initial_count - final_count} zduplikowanych rekordów.")
        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Obsługuje brakujące wartości w kluczowych kolumnach.
        Usuwa wiersze bez ceny i metrażu, dla innych stosuje imputację wartością modalną lub medianą.
        """
        df = df.dropna(subset=["price", "area"])

        if "rooms" in df.columns:
            df["rooms"] = df["rooms"].fillna(df["rooms"].median())
        if "floor" in df.columns:
            df["floor"] = df["floor"].fillna(0)
        if "year_built" in df.columns:
            df["year_built"] = df["year_built"].fillna(df["year_built"].median())

        return df

    def normalize_price(self, df: pd.DataFrame) -> pd.DataFrame:
        """Konwertuje kolumnę ceny do formatu float oraz czyści znaki walutowe."""
        try:
            if df["price"].dtype == object:
                df["price"] = df["price"].astype(str).str.replace(r"[^\d.,]", "", regex=True)
                df["price"] = df["price"].str.replace(",", ".")
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            df = df[df["price"] > 0]
        except Exception as e:
            logger.error(f"Błąd podczas normalizacji cen: {e}")
        return df

    def normalize_area(self, df: pd.DataFrame) -> pd.DataFrame:
        """Konwertuje kolumnę powierzchni do formatu float."""
        try:
            if df["area"].dtype == object:
                df["area"] = df["area"].astype(str).str.replace(r"[^\d.,]", "", regex=True)
                df["area"] = df["area"].str.replace(",", ".")
            df["area"] = pd.to_numeric(df["area"], errors="coerce")
            df = df[df["area"] > 0]
        except Exception as e:
            logger.error(f"Błąd podczas normalizacji powierzchni: {e}")
        return df

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Uruchamia pełny potok czyszczenia danych.

        Args:
            df (pd.DataFrame): Surowy obiekt DataFrame.

        Returns:
            pd.DataFrame: Oczyszczony i ustrukturyzowany zestaw danych.
        """
        if df.empty:
            logger.warning("Przekazano pusty DataFrame do procesu czyszczenia.")
            return df

        logger.info("Rozpoczęcie procedury czyszczenia danych...")

        for col in self.required_columns:
            if col not in df.columns:
                df[col] = np.nan

        df = df.copy()
        df = self.remove_duplicates(df)
        df = self.normalize_price(df)
        df = self.normalize_area(df)
        df = self.handle_missing_values(df)

        # Zachowujemy oryginalne skróty z Ames Housing Dataset, np. NAmes, NoRidge, IDOTRR, C (all), 1Fam.
        df["city"] = df["city"].astype(str).str.strip()
        df["district"] = df["district"].astype(str).str.strip()
        df["property_type"] = df["property_type"].astype(str).str.strip()

        df["rooms"] = df["rooms"].astype(int)
        df["floor"] = df["floor"].astype(int)
        df["year_built"] = df["year_built"].astype(int)

        df["price_per_m2"] = np.round(df["price"] / df["area"], 2)

        logger.info(f"Proces czyszczenia zakończony pomyślnie. Pozostało {len(df)} rekordów.")
        return df[self.required_columns + ["price_per_m2"]]
