#!/usr/bin/env python3
"""
Główny punkt wejścia do aplikacji Real Estate Data Analysis.
Inicjalizuje system logowania, sprawdza strukturę katalogów i uruchamia interfejs GUI.
"""

import os
import logging
import sys
from pathlib import Path

# Dodanie katalogu głównego do ścieżki wyszukiwania modułów Python
sys.path.append(str(Path(__file__).resolve().parent))

from src.gui.app import App


def setup_logging() -> None:
    """Konfiguruje globalny system logowania dla całej aplikacji."""
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        ]
    )


def initialize_directories() -> None:
    """Tworzy wymaganą strukturę katalogów, jeśli nie istnieje."""
    base_dir = Path(__file__).resolve().parent
    directories = [
        base_dir / "src" / "data" / "raw",
        base_dir / "src" / "data" / "processed",
        base_dir / "assets" / "icons",
        base_dir / "docs" / "screenshots",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Główna funkcja uruchomieniowa aplikacji."""
    setup_logging()
    logger = logging.getLogger("Main")
    logger.info("Uruchamianie aplikacji Real Estate Data Analysis Python...")

    try:
        initialize_directories()
        app = App()
        app.mainloop()
        logger.info("Aplikacja została zamknięta prawidłowo.")
    except Exception as e:
        logger.critical(f"Krytyczny błąd podczas działania aplikacji: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()