# Real Estate Data Analysis Python

Projekt zaliczeniowy z przedmiotu Zaawansowane programowanie w Pythonie.

Celem projektu jest stworzenie aplikacji w języku Python do analizy danych dotyczących rynku nieruchomości. Aplikacja będzie pobierać dane dynamicznie z internetu, przetwarzać je z użyciem bibliotek pandas/numpy oraz prezentować wyniki w interfejsie graficznym przygotowanym w tkinter.

## Planowane funkcjonalności

- pobieranie danych z internetu/API,
- czyszczenie i przetwarzanie danych,
- analiza cen nieruchomości,
- porównanie ofert według lokalizacji,
- generowanie wykresów z użyciem matplotlib,
- interfejs graficzny w tkinter,
- dokumentacja projektu.

## Technologie

- Python
- pandas
- numpy
- matplotlib
- tkinter
- requests

## Uruchomienie projektu

Instrukcja zostanie uzupełniona w trakcie realizacji projektu.

## Struktura projektu / TO DO

- zaktualizowano 08.06.2026 (12:20) [done]
- uzgodnić strukturę projektu. Czy (`real_estate_analysis.py`, `data_loader.py`, `charts.py`) mają pozostać? [done]
- Utworzono foldery techniczne. Należy rozważyć, czy je pozostawić (icons/, screenshots/, raw/, processed/) [done]
- > **Status projektu:** Utworzono kompletną strukturę katalogów i pliki bazowe, które stanowią szkielet aplikacji. 
  > Poszczególne moduły są obecnie puste i będą sukcesywnie uzupełniane kodem w kolejnych etapach wdrożenia. [done]


## Wdrażanie kodu i korekta błędów

- usunięto pliki uznając je za nie potrzebne  (`real_estate_analysis.py`, `data_loader.py`, `charts.py`),

## Wdrażanie warstwy danych DATA LAYER

- ustalono wstępne .gitignore
- uzupełniono plik main.py z nastawieniem na jego możliwe przyszłe zmiany
- wdrożono moduł DATA LAYER zawierający cache.py, cleaner.py oraz fetcher.py