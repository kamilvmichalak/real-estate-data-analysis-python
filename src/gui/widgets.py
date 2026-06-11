"""
Moduł zawierający niestandardowe komponenty graficzne (Widgets) wielokrotnego użytku.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class StatusBar(tk.Frame):
    """Pasek statusu wyświetlający bieżące komunikaty systemowe na dole ekranu."""

    def __init__(self, parent: tk.Misc, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.config(bd=1, relief=tk.SUNKEN)
        self.label = tk.Label(self, text="System gotowy do pracy.", anchor=tk.W, font=("Arial", 9))
        self.label.pack(fill=tk.X, padx=5, pady=2)

    def set_text(self, text: str) -> None:
        """Aktualizuje tekst na pasku stanu."""
        self.label.config(text=text)


class FilterFrame(tk.LabelFrame):
    """Panel filtrujący umożliwiający szybką selekcję miast."""

    def __init__(self, parent: tk.Misc, on_change_callback: Callable[[str], None], **kwargs) -> None:
        super().__init__(parent, text=" Szybkie Filtrowanie Danych ", **kwargs)

        tk.Label(self, text="Wybierz miasto:").pack(side=tk.LEFT, padx=5, pady=5)

        self.combo = ttk.Combobox(self,
                                  values=["Wszystkie", "Warszawa", "Kraków", "Wrocław", "Poznań", "Gdańsk", "Łódź"],
                                  state="readonly")
        self.combo.set("Wszystkie")
        self.combo.pack(side=tk.LEFT, padx=5, pady=5)

        self.combo.bind("<<ComboboxSelected>>", lambda e: on_change_callback(self.combo.get()))


class LoadingOverlay:
    """Ekran blokujący interfejs użytkownika podczas asynchronicznego pobierania danych."""

    def __init__(self, parent: tk.Toplevel | tk.Tk) -> None:
        self.parent = parent
        self.overlay: Optional[tk.Toplevel] = None

    def show(self, text: str = "Pobieranie danych... Proszę czekać...") -> None:
        """Wyświetla modalne okno ładowania."""
        if self.overlay:
            return

        self.overlay = tk.Toplevel(self.parent)
        self.overlay.withdraw()  # Ukryj na czas konfiguracji rozłożenia
        self.overlay.title("Przetwarzanie")
        self.overlay.geometry("300x100")
        self.overlay.resizable(False, False)
        self.overlay.transient(self.parent)
        self.overlay.grab_set()

        # Centrowanie względem okna nadrzędnego
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 150
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 50
        self.overlay.geometry(f"+{x}+{y}")

        frame = tk.Frame(self.overlay, padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(frame, text=text, font=("Arial", 10, "bold"))
        lbl.pack(pady=5)

        progress = ttk.Progressbar(frame, mode="indeterminate")
        progress.pack(fill=tk.X, padx=10, pady=5)
        progress.start(10)

        self.overlay.deiconify()
        self.parent.update_idletasks()

    def hide(self) -> None:
        """Zamyka okno ładowania i przywraca dostęp do aplikacji."""
        if self.overlay:
            self.overlay.grab_release()
            self.overlay.destroy()
            self.overlay = None


class ToolTip:
    """Dynamiczna etykieta pomocnicza typu ToolTip po najechaniu kursorem myszy."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip_window: Optional[tk.Toplevel] = None

        self.widget.bind("<Enter>", lambda e: self.show_tip())
        self.widget.bind("<Leave>", lambda e: self.hide_tip())

    def show_tip(self) -> None:
        """Generuje pływające okienko z podpowiedzią."""
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self) -> None:
        """Niszczy okienko podpowiedzi."""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()