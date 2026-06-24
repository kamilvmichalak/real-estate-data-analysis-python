# Real Estate Data Analysis Python

Projekt zaliczeniowy z przedmiotu **Zaawansowane programowanie w Pythonie**.

Aplikacja desktopowa służy do pobierania, czyszczenia, analizy i wizualizacji danych dotyczących rynku nieruchomości. Dane są pobierane z internetu z wykorzystaniem zbioru **OpenML Ames Housing Dataset**, a następnie mapowane do wspólnego formatu używanego przez aplikację.

## Cel projektu

Celem projektu jest przygotowanie aplikacji w języku Python, która:

- pobiera dane dotyczące nieruchomości z zewnętrznego źródła,
- przetwarza i czyści dane z wykorzystaniem `pandas` oraz `numpy`,
- umożliwia tabelaryczny podgląd danych w interfejsie graficznym,
- generuje raporty statystyczne dotyczące cen i lokalizacji,
- tworzy wykresy i wizualizacje z użyciem `matplotlib` oraz `seaborn`,
- umożliwia eksport danych do pliku CSV oraz zapis wykresów do PNG.

## Źródło danych

Aplikacja korzysta z datasetu **Ames Housing Dataset** dostępnego przez OpenML. Dane są pobierane za pomocą funkcji `fetch_openml` z biblioteki `scikit-learn`.

W projekcie dane źródłowe są mapowane do następującego formatu:

| Kolumna aplikacji | Znaczenie |
|---|---|
| `title` | generowany tytuł oferty, np. `House in CollgCr` |
| `city` | lokalizacja / neighborhood, np. `CollgCr`, `NAmes`, `NoRidge` |
| `district` | strefa zagospodarowania, np. `RL`, `RM`, `FV`, `C (all)` |
| `property_type` | typ nieruchomości, np. `1Fam`, `Duplex`, `TwnhsE` |
| `area` | powierzchnia w metrach kwadratowych |
| `rooms` | liczba pokoi nad poziomem gruntu |
| `floor` | uproszczona liczba kondygnacji wyliczona na podstawie stylu domu |
| `year_built` | rok budowy |
| `price` | cena sprzedaży w USD |
| `date_added` | data zbudowana na podstawie miesiąca i roku sprzedaży |
| `price_per_m2` | cena za metr kwadratowy w USD/m² |

Wartości takie jak `RL`, `RM` lub `C (all)` są oryginalnymi skrótami ze zbioru Ames Housing Dataset. Przykładowo `RL` oznacza Residential Low Density, `RM` oznacza Residential Medium Density, a `C (all)` oznacza Commercial.

Jeżeli pobranie danych z OpenML się nie powiedzie, aplikacja korzysta z lokalnego generatora danych syntetycznych jako mechanizmu awaryjnego.

## Główne funkcjonalności

### 1. Pobieranie i cache danych

Po kliknięciu przycisku **Pobierz dane** aplikacja:

1. pobiera dane z OpenML,
2. mapuje kolumny datasetu do formatu aplikacji,
3. zapisuje dane surowe do `src/data/raw/raw_offers.csv`,
4. czyści dane,
5. zapisuje dane przetworzone do `src/data/processed/processed_offers.csv`,
6. przekazuje oczyszczony `DataFrame` do zakładek GUI.

Przy kolejnym uruchomieniu aplikacja próbuje najpierw wczytać dane z lokalnej pamięci podręcznej.

### 2. Baza danych ofert

Zakładka **Baza danych ofert** umożliwia:

- podgląd danych w tabeli,
- filtrowanie ofert według lokalizacji,
- sortowanie kolumn po kliknięciu nagłówka,
- eksport aktualnego zestawu danych do pliku CSV.

### 3. Raporty statystyczne

Zakładka **Raporty statystyczne** generuje tekstowy raport obejmujący m.in.:

- średnią cenę według lokalizacji,
- medianę ceny według lokalizacji,
- średnią cenę za metr kwadratowy,
- średnią cenę według typu nieruchomości,
- najtańsze i najdroższe lokalizacje według ceny USD/m²,
- dynamikę zmian cen w czasie,
- liczbę ofert w ujęciu kwartalnym,
- macierz korelacji cech numerycznych.

Pole **Limit lokalizacji w raporcie** ogranicza liczbę lokalizacji pokazywanych w sekcjach raportu.

### 4. Wizualizacje graficzne

Zakładka **Wizualizacje graficzne** pozwala wygenerować następujące wykresy:

- średnia cena według lokalizacji,
- liczba ofert według typu nieruchomości,
- wykres rozrzutu ceny względem powierzchni z linią regresji,
- mapa ciepła korelacji cech,
- histogram rozkładu cen,
- wykres pudełkowy cen dla najczęstszych lokalizacji,
- trend czasowy napływu ogłoszeń.

Wygenerowany wykres można zapisać jako plik PNG.

## Technologie

Projekt wykorzystuje:

- Python,
- tkinter,
- pandas,
- numpy,
- matplotlib,
- seaborn,
- scikit-learn,
- requests,
- beautifulsoup4.

## Instalacja i uruchomienie

### 1. Pobranie projektu

```bash
git clone https://github.com/kamilvmichalak/real-estate-data-analysis-python.git
cd real-estate-data-analysis-python
```

### 2. Utworzenie środowiska wirtualnego

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchomienie aplikacji

```bash
python main.py
```

Po uruchomieniu aplikacji należy kliknąć **Pobierz dane**, aby zsynchronizować dane z OpenML. Po pierwszym pobraniu dane zostaną zapisane w cache i będą mogły zostać wczytane lokalnie przy kolejnym uruchomieniu.

## Struktura projektu

```text
real-estate-data-analysis-python/
├── main.py
├── requirements.txt
├── README.md
├── logs/
├── src/
│   ├── analysis/
│   │   ├── correlation.py
│   │   ├── location_analysis.py
│   │   ├── price_analysis.py
│   │   └── trend_analysis.py
│   ├── data/
│   │   ├── cache.py
│   │   ├── cleaner.py
│   │   ├── fetcher.py
│   │   ├── raw/
│   │   └── processed/
│   ├── gui/
│   │   ├── app.py
│   │   ├── tab_analysis.py
│   │   ├── tab_charts.py
│   │   ├── tab_data.py
│   │   └── widgets.py
│   └── visualization/
│       ├── bar_charts.py
│       ├── heatmap.py
│       ├── histograms.py
│       ├── line_charts.py
│       └── scatter_plots.py
```

## Krótki opis architektury

Aplikacja jest podzielona na kilka warstw:

- `main.py` — punkt wejścia, konfiguracja logowania i katalogów roboczych,
- `src/gui` — interfejs użytkownika w tkinter,
- `src/data` — pobieranie danych, czyszczenie i obsługa cache,
- `src/analysis` — logika raportów statystycznych,
- `src/visualization` — funkcje generujące wykresy matplotlib/seaborn.

Dane są przechowywane w aplikacji jako obiekt `pandas.DataFrame`, który po pobraniu i oczyszczeniu jest przekazywany do wszystkich zakładek GUI.

## Uwagi dotyczące danych

Dataset Ames Housing opisuje nieruchomości z Ames w stanie Iowa. Wartości lokalizacji i stref są skrótami pochodzącymi z oryginalnego zbioru danych. Z tego powodu w aplikacji używane są określenia **Lokalizacja** i **Strefa**, a nie polskie miasta i dzielnice.

Ceny są wyrażone w USD, a powierzchnia została przeliczona ze stóp kwadratowych na metry kwadratowe.

## Autor

Kamil Michalak
Oskar Wojtkowiak
