"""
Główny kontroler aplikacji (Main Controller / Window), spinający logikę biznesową z interfejsem użytkownika.
Zarządza operacjami asynchronicznymi w tle.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
import pandas as pd

from data.fetcher import RealEstateFetcher
from data.cleaner import DataCleaner
from data.cache import DataCache

from .tab_data import DataTab
from .tab_analysis import AnalysisTab
from .tab_charts import ChartsTab
from .widgets import StatusBar, LoadingOverlay

logger = logging.getLogger(__name__)


class App(tk.Tk):
    """Główna klasa aplikacji rozszerzająca bazowe okno tk.Tk."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Real Estate Data Analysis Dashboard v1.0")
        self.geometry("1100x700")
        self.minimum_size_width = 1000
        self.minimum_size_height = 650
        self.minsize(self.minimum_size_width, self.minimum_size_height)

        # Inicjalizacja warstwy logiki danych (Zgodnie z SOLID / DI)
        self.fetcher = RealEstateFetcher()
        self.cleaner = DataCleaner()
        self.cache = DataCache()

        self.loaded_dataframe = pd.DataFrame()
        self.loading_overlay = LoadingOverlay(self)

        self._assemble_layout()
        self._load_initial_cache()

    def _assemble_layout(self) -> None:
        """Tworzy szkielet widoków, kart i paska statusu."""
        # Pasek narzędziowy / Zakładki (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Inicjalizacja poszczególnych kart interfejsu
        self.tab_data = DataTab(self.notebook, fetch_callback=self.trigger_async_fetch)
        self.tab_analysis = AnalysisTab(self.notebook)
        self.tab_charts = ChartsTab(self.notebook)

        self.notebook.add(self.tab_data, text="  Baza danych ofert  ")
        self.notebook.add(self.tab_analysis, text="  Raporty statystyczne  ")
        self.notebook.add(self.tab_charts, text="  Wizualizacje graficzne  ")

        # Integracja paska stanu
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_initial_cache(self) -> None:
        """Wczytuje z pamięci lokalnej ostatnio przetworzone dane przy starcie."""
        df = self.cache.load_cached_data(processed=True)
        if not df.empty:
            self.loaded_dataframe = df
            self._propagate_data_to_tabs()
            self.status_bar.set_text("Załadowano dane z lokalnej pamięci podręcznej (Cache).")

    def trigger_async_fetch(self, source_mode: str) -> None:
        """Uruchamia proces pobierania danych w dedykowanym, bezpiecznym wątku."""
        self.loading_overlay.show("Pobieranie i przetwarzanie danych rynkowych...")
        self.status_bar.set_text(f"Pobieranie danych w tle z wykorzystaniem modułu: {source_mode.upper()}...")

        # Izolacja wielowątkowa
        worker = threading.Thread(target=self._async_fetch_worker, args=(source_mode,), daemon=True)
        worker.start()

    def _async_fetch_worker(self, source_mode: str) -> None:
        """Praca wykonywana w tle w celu zachowania responsywności interfejsu graficznego."""
        try:
            # 1. Pobieranie danych
            raw_df = self.fetcher.fetch_data(source_type=source_mode)
            if raw_df.empty:
                raise ValueError("Źródło danych zwróciło pusty zestaw rekordów.")

            self.cache.save_raw_data(raw_df)

            # 2. Czyszczenie i Transformacja
            cleaned_df = self.cleaner.clean(raw_df)
            if cleaned_df.empty:
                raise ValueError("Brak rekordów spełniających kryteria po przeprowadzeniu procesu czyszczenia.")

            self.cache.save_processed_data(cleaned_df)
            self.loaded_dataframe = cleaned_df

            # Modyfikacja widoku bezpieczna z poziomu wątku roboczego
            self.after(0, self._on_fetch_success)


        except Exception as e:

            logger.error(f"Wyjątek w wątku roboczym pobierania: {e}", exc_info=True)

            # ZAPISUJEMY TREŚĆ BŁĘDU DO ZMIENNEJ TEKSTOWEJ

            error_msg = str(e)

            self.after(0, lambda: self._on_fetch_failure(error_msg))

    def _on_fetch_success(self) -> None:
        self.loading_overlay.hide()
        self._propagate_data_to_tabs()
        self.status_bar.set_text(f"Sukces! Baza zsynchronizowana. Załadowano: {len(self.loaded_dataframe)} ogłoszeń.")
        messagebox.showinfo("Synchronizacja", "Dane zostały pomyślnie pobrane, oczyszczone i zaktualizowane w pamięci RAM!")

    def _on_fetch_failure(self, error_message: str) -> None:
        self.loading_overlay.hide()
        self.status_bar.set_text("Błąd podczas odświeżania danych rynkowych.")
        messagebox.showerror("Błąd pobierania", f"Wystąpił problem krytyczny podczas pobierania danych:\n{error_message}")

    def _propagate_data_to_tabs(self) -> None:
        """Dystrybuuje zaktualizowany obiekt DataFrame do niezależnych modułów UI."""
        self.tab_data.update_data(self.loaded_dataframe)
        self.tab_analysis.set_data(self.loaded_dataframe)
        self.tab_charts.set_data(self.loaded_dataframe)