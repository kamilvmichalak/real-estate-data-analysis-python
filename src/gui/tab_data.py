"""Zakładka z tabelarycznym podglądem danych oraz eksportem CSV."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from typing import Callable
from .widgets import FilterFrame


class DataTab(tk.Frame):
    """Panel reprezentujący zakładkę danych w interfejsie graficznym."""

    def __init__(self, parent: ttk.Notebook, fetch_callback: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.fetch_callback = fetch_callback
        self.full_df: pd.DataFrame = pd.DataFrame()
        self._build_ui()

    def _build_ui(self) -> None:
        control_frame = tk.LabelFrame(self, text=" Zarządzanie źródłami danych ", padx=10, pady=5)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Źródło danych: OpenML Ames Housing Dataset (USA)",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=5)

        self.btn_fetch = tk.Button(
            control_frame,
            text="Pobierz dane",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
            command=lambda: self.fetch_callback("openml")
        )
        self.btn_fetch.pack(side=tk.RIGHT, padx=10)

        self.filter_frame = FilterFrame(self, on_change_callback=self.filter_data)
        self.filter_frame.pack(fill=tk.X, padx=10, pady=5)

        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = (
            "title", "city", "district", "property_type", "area",
            "rooms", "floor", "year_built", "price", "price_per_m2"
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        headers = {
            "title": "Tytuł ogłoszenia",
            "city": "Lokalizacja",
            "district": "Strefa",
            "property_type": "Typ",
            "area": "Pow. (m²)",
            "rooms": "Pokoje",
            "floor": "Kondygnacje",
            "year_built": "Rok budowy",
            "price": "Cena (USD)",
            "price_per_m2": "USD/m²",
        }
        for col, text in headers.items():
            self.tree.heading(col, text=text, command=lambda c=col: self._sort_treeview(c, False))
            self.tree.column(col, width=90, anchor=tk.CENTER if col != "title" else tk.W)

        self.tree.column("title", width=250)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = tk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=5, side=tk.BOTTOM)

        self.btn_export = tk.Button(
            action_frame,
            text="Eksportuj do CSV...",
            bg="#2196F3",
            fg="white",
            command=self.export_to_csv
        )
        self.btn_export.pack(side=tk.LEFT, pady=2)

        self.lbl_counter = tk.Label(action_frame, text="Liczba rekordów: 0", font=("Arial", 9, "italic"))
        self.lbl_counter.pack(side=tk.RIGHT, pady=2)

    def update_data(self, df: pd.DataFrame) -> None:
        """Ładuje i prezentuje nowy zestaw danych w tabeli."""
        self.full_df = df

        if not df.empty and "city" in df.columns:
            self.filter_frame.set_options(df["city"].dropna().astype(str).tolist())
        else:
            self.filter_frame.set_options([])

        self.filter_data("Wszystkie")

    def filter_data(self, city_filter: str) -> None:
        """Filtruje wyświetlane rekordy na podstawie wybranej lokalizacji."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.full_df.empty:
            self.lbl_counter.config(text="Liczba rekordów: 0")
            return

        if city_filter == "Wszystkie":
            display_df = self.full_df
        else:
            display_df = self.full_df[self.full_df["city"].str.lower() == city_filter.lower()]

        for _, row in display_df.iterrows():
            self.tree.insert("", tk.END, values=(
                row.get("title", ""), row.get("city", ""), row.get("district", ""),
                row.get("property_type", ""), row.get("area", ""), row.get("rooms", ""),
                row.get("floor", ""), row.get("year_built", ""), row.get("price", ""),
                row.get("price_per_m2", "")
            ))

        self.lbl_counter.config(text=f"Liczba rekordów: {len(display_df)} (odfiltrowane z {len(self.full_df)})")

    def export_to_csv(self) -> None:
        """Umożliwia użytkownikowi zapisanie aktualnego zbioru danych w dowolnej lokalizacji."""
        if self.full_df.empty:
            messagebox.showwarning("Brak danych", "Nie ma żadnych danych do wyeksportowania.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Pliki CSV", "*.csv")])
        if file_path:
            try:
                self.full_df.to_csv(file_path, index=False, encoding="utf-8")
                messagebox.showinfo("Sukces", f"Dane zostały pomyślnie zapisane w pliku:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")

    def _sort_treeview(self, col: str, reverse: bool) -> None:
        """Sortuje zawartość kolumny po kliknięciu nagłówka."""
        values = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]

        def sort_key(item):
            value = item[0]
            try:
                return 0, float(str(value).replace(" ", "").replace(",", "."))
            except ValueError:
                return 1, str(value).lower()

        values.sort(key=sort_key, reverse=reverse)

        for index, (_, item) in enumerate(values):
            self.tree.move(item, "", index)

        self.tree.heading(col, command=lambda: self._sort_treeview(col, not reverse))
