"""
Implementacja zakładki generującej tekstowe zestawienia statystyczne rynku nieruchomości.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
from src.analysis.price_analysis import PriceAnalysis
from src.analysis.location_analysis import LocationAnalysis
from src.analysis.trend_analysis import TrendAnalysis
from src.analysis.correlation import CorrelationAnalysis


class AnalysisTab(tk.Frame):
    """Panel reprezentujący zakładkę 'Analizy'."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent)
        self.df: pd.DataFrame = pd.DataFrame()
        self._build_ui()

    def _build_ui(self) -> None:
        # Lewy panel wyboru rodzaju analizy
        left_panel = tk.LabelFrame(self, text=" Wybór zakresu analiz rynkowych ", width=250, padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.check_price = tk.BooleanVar(value=True)
        self.check_location = tk.BooleanVar(value=True)
        self.check_trend = tk.BooleanVar(value=True)
        self.check_corr = tk.BooleanVar(value=True)

        tk.Checkbutton(left_panel, text="Analiza cenowa (średnie, mediany)", variable=self.check_price).pack(
            anchor=tk.W, pady=5)
        tk.Checkbutton(left_panel, text="Analiza lokalizacji (Extreme places)", variable=self.check_location).pack(
            anchor=tk.W, pady=5)
        tk.Checkbutton(left_panel, text="Analiza trendów i wzrostów", variable=self.check_trend).pack(anchor=tk.W,
                                                                                                      pady=5)
        tk.Checkbutton(left_panel, text="Obliczanie macierzy korelacji", variable=self.check_corr).pack(anchor=tk.W,
                                                                                                        pady=5)

        # Panel parametrów krańcowych
        param_frame = tk.Frame(left_panel)
        param_frame.pack(fill=tk.X, pady=15)
        tk.Label(param_frame, text="Limit rekordów lokalizacji:").pack(side=tk.LEFT)
        self.entry_limit = tk.Entry(param_frame, width=5)
        self.entry_limit.insert(0, "5")
        self.entry_limit.pack(side=tk.LEFT, padx=5)

        self.btn_calc = tk.Button(left_panel, text="Uruchom analizę", bg="#FF9800", fg="white",
                                  font=("Arial", 10, "bold"), command=self.run_analysis)
        self.btn_calc.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        # Prawy panel tekstowy prezentacji raportu końcowego
        right_panel = tk.LabelFrame(self, text=" Wygenerowany Raport Analityczny (Zgodnie z SOLID) ")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.txt_report = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, font=("Consolas", 10))
        self.txt_report.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_report.insert(tk.END,
                               "Załaduj dane, wybierz zakresy analiz i naciśnij 'Uruchom analizę' aby wygenerować raport rynkowy.")

    def set_data(self, df: pd.DataFrame) -> None:
        """Przekazuje aktualną bazę danych do obszaru analiz."""
        self.df = df

    def run_analysis(self) -> None:
        """Zbiera zaznaczone analizy statystyczne i składa je w czytelny raport tekstowy."""
        if self.df.empty:
            self.txt_report.delete(1.0, tk.END)
            self.txt_report.insert(tk.END,
                                   "BŁĄD: Brak załadowanych danych w pamięci aplikacji! Pobierz dane w pierwszej zakładce.")
            return

        try:
            limit = int(self.entry_limit.get())
        except ValueError:
            limit = 5

        report = []
        report.append("======================================================================")
        report.append("          RAPORT ANALITYCZNY RYNKU NIERUCHOMOŚCI - PYTHON 3.12+       ")
        report.append("======================================================================\n")

        if self.check_price.get():
            report.append("--- 1. STATYSTYKI CENOWE ---")
            report.append("Średnia cena w miastach:")
            report.append(PriceAnalysis.average_price_by_city(self.df).to_string())
            report.append("\nMediana ceny w miastach:")
            report.append(PriceAnalysis.median_price_by_city(self.df).to_string())
            report.append("\nŚrednia cena za metr kwadratowy w miastach:")
            report.append(PriceAnalysis.average_price_per_square_meter(self.df).to_string())
            report.append("\nŚrednia cena według typu nieruchomości:")
            report.append(PriceAnalysis.average_price_by_property_type(self.df).to_string())
            report.append("-" * 50 + "\n")

        if self.check_location.get():
            report.append("--- 2. ANALIZA LOKALIZACYJNA (TOP OBRĘBY) ---")
            report.append(f"Najtańsze lokalizacje (Top {limit} dzielnic wg ceny PLN/m²):")
            report.append(LocationAnalysis.cheapest_locations(self.df, limit).to_string(index=False))
            report.append(f"\nNajdroższe lokalizacje (Top {limit} dzielnic wg ceny PLN/m²):")
            report.append(LocationAnalysis.most_expensive_locations(self.df, limit).to_string(index=False))
            report.append("-" * 50 + "\n")

        if self.check_trend.get():
            report.append("--- 3. DYNAMIKA RYNKU I TRENDY CZASOWE ---")
            growth = TrendAnalysis.market_growth_rate(self.df)
            report.append(f"Wskaźnik dynamiki wzrostu cen (ostatni vs pierwszy okres): {growth}%")
            report.append("\nLiczba dodanych ofert w ujęciu kwartalnym:")
            report.append(TrendAnalysis.offers_per_quarter(self.df).to_string())
            report.append("-" * 50 + "\n")

        if self.check_corr.get():
            report.append("--- 4. MACIERZ KORELACJI SPECYFIKACJI ---")
            report.append(CorrelationAnalysis.calculate_correlation_matrix(self.df).to_string())
            report.append("-" * 50 + "\n")

        self.txt_report.delete(1.0, tk.END)
        self.txt_report.insert(tk.END, "\n".join(report))