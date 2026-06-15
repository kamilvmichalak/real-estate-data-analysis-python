"""
Moduł odpowiedzialny za lokalny zapis oraz odczyt danych (Cache-ing) w formacie CSV.
Zapobiega nadmiernemu obciążaniu zewnętrznych serwisów internetowych.
"""

import os
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class DataCache:
    """Klasa zarządzająca lokalnymi plikami pamięci podręcznej."""

    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parent
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"

        # Tworzenie katalogów, jeśli nie istnieją
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        self.raw_file = self.raw_dir / "raw_offers.csv"
        self.processed_file = self.processed_dir / "processed_offers.csv"

    def save_raw_data(self, df: pd.DataFrame) -> bool:
        """Zapisuje surowe dane pobrane z internetu."""
        try:
            df.to_csv(self.raw_file, index=False, encoding="utf-8")
            logger.info(f"Surowe dane zostały zapisane w cache: {self.raw_file}")
            return True
        except Exception as e:
            logger.error(f"Błąd zapisu surowego cache: {e}")
            return False

    def save_processed_data(self, df: pd.DataFrame) -> bool:
        """Zapisuje przefiltrowane i wyczyszczone dane rynkowe."""
        try:
            df.to_csv(self.processed_file, index=False, encoding="utf-8")
            logger.info(f"Oczyszczone dane zostały zapisane w cache: {self.processed_file}")
            return True
        except Exception as e:
            logger.error(f"Błąd zapisu przetworzonego cache: {e}")
            return False

    def load_cached_data(self, processed: bool = True) -> pd.DataFrame:
        """
        Wczytuje dane z lokalnego pliku cache.

        Args:
            processed (bool): Jeśli True, wczytuje dane oczyszczone, w przeciwnym wypadku surowe.
        """
        target_file = self.processed_file if processed else self.raw_file

        if not target_file.exists():
            logger.warning(f"Brak pliku cache: {target_file}. Wymagane pobieranie sieciowe.")
            return pd.DataFrame()

        try:
            df = pd.read_csv(target_file, encoding="utf-8")
            logger.info(f"Pomyślnie załadowano dane z cache: {target_file} ({len(df)} wierszy).")
            return df
        except Exception as e:
            logger.error(f"Nie udało się odczytać pliku cache {target_file}: {e}")
            return pd.DataFrame()