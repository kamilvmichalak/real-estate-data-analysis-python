"""
Implementacja zakładki rysującej i eksportującej wykresy matplotlib w oknie tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from src.visualization.bar_charts import average_price_by_city_chart, offers_per_type_chart
from src.visualization.scatter_plots import area_vs_price_chart
from src.visualization.heatmap import correlation_heatmap
from src.visualization.histograms import price_distribution_histogram, price_boxplot
from src.visualization.line_charts import offers_trend_chart


class ChartsTab(tk.Frame):
    """Panel reprezentujący zakładkę 'Wykresy'."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent)
        self.df: pd.DataFrame = pd.DataFrame()
        self.current_fig: Optional[Figure] = None
        self.canvas: Optional[FigureCanvasTkAgg] = None
        self.toolbar: Optional[NavigationToolbar2Tk] = None
        self._build_ui()

    def _build_ui(self) -> None:
        left_frame = tk.LabelFrame(self, text=" Lista dostępnych wizualizacji ", width=220, padx=5, pady=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.chart_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, font=("Arial", 9))
        self.charts_map = {
            "Średnia cena według lokalizacji": average_price_by_city_chart,
            "Liczba ofert wg typu": offers_per_type_chart,
            "Wykres rozrzutu (Cena vs Powierzchnia)": area_vs_price_chart,
            "Mapa ciepła korelacji cech": correlation_heatmap,
            "Histogram rozkładu cen": price_distribution_histogram,
            "Wykres pudełkowy (Outliery)": price_boxplot,
            "Trend czasowy napływu ogłoszeń": offers_trend_chart
        }

        for name in self.charts_map.keys():
            self.chart_listbox.insert(tk.END, name)

        self.chart_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.chart_listbox.bind("<<ListboxSelect>>", lambda e: self.render_selected_chart())

        self.btn_save_png = tk.Button(left_frame, text="Zapisz wykres jako PNG", bg="#009688", fg="white",
                                      command=self.save_chart_as_png)
        self.btn_save_png.pack(fill=tk.X, pady=5)

        self.plot_container = tk.LabelFrame(self, text=" Obszar renderowania graficznego (Matplotlib Engine) ")
        self.plot_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_placeholder = tk.Label(self.plot_container,
                                        text="Wybierz wykres z listy po lewej stronie, aby wyświetlić wizualizację.",
                                        font=("Arial", 10, "italic"))
        self.lbl_placeholder.pack(expand=True)

    def set_data(self, df: pd.DataFrame) -> None:
        """Przekazuje dane i odświeża bieżący wykres."""
        self.df = df
        self.render_selected_chart()

    def render_selected_chart(self) -> None:
        """Pobiera zaznaczoną pozycję, czyści stare płótno i osadza nowy wykres."""
        selection = self.chart_listbox.curselection()
        if not selection or self.df.empty:
            return

        if self.lbl_placeholder:
            self.lbl_placeholder.pack_forget()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.toolbar:
            self.toolbar.destroy()

        chart_name = self.chart_listbox.get(selection[0])
        chart_function = self.charts_map[chart_name]

        self.current_fig = chart_function(self.df)

        self.canvas = FigureCanvasTkAgg(self.current_fig, master=self.plot_container)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
        self.toolbar.update()

        self.canvas.draw()

    def save_chart_as_png(self) -> None:
        """Zapisuje bieżący stan wykresu bezpośrednio do pliku graficznego rasterowego."""
        if not self.current_fig:
            messagebox.showwarning("Brak rysunku", "Najpierw wygeneruj wykres wybierając go z listy.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Obrazy PNG", "*.png")])
        if file_path:
            try:
                self.current_fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Zapisano", f"Wykres został zapisany pomyślnie w:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać grafiki: {e}")
