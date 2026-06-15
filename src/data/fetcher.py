import logging
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml

logger = logging.getLogger(__name__)


class RealEstateFetcher:
    """
    Pobiera realne dane nieruchomości z OpenML Ames Housing Dataset.

    Dane źródłowe mają inną strukturę niż aplikacja, dlatego są mapowane
    do wspólnego formatu:
    title, city, district, property_type, area, rooms, floor, year_built, price, date_added.
    """

    def __init__(self) -> None:
        self.openml_data_id = 42165
        self.dataset_name = "house_prices"
        self.dataset_version = 1

    def fetch_data(self, source_type: str = "openml") -> pd.DataFrame:
        """
        Pobiera dane z OpenML. Jeśli pobieranie się nie powiedzie,
        uruchamia lokalny generator danych syntetycznych.
        """
        logger.info("Inicjalizacja pobierania danych z OpenML Ames Housing Dataset...")

        try:
            raw_df = self._fetch_openml_dataset()
            normalized_df = self._normalize_openml_house_prices(raw_df)

            if normalized_df.empty:
                raise ValueError("Dataset OpenML został pobrany, ale po mapowaniu jest pusty.")

            logger.info(f"Sukces! Pobrano i przemapowano {len(normalized_df)} rekordów z OpenML.")
            return normalized_df

        except Exception as e:
            logger.error(f"Nie udało się pobrać danych z OpenML: {e}", exc_info=True)
            logger.warning("Uruchamianie lokalnego generatora danych syntetycznych...")
            return self._generate_synthetic_data()

    def _fetch_openml_dataset(self) -> pd.DataFrame:
        """
        Pobiera dataset z OpenML. Najpierw próbuje po ID, a jeśli to się nie uda,
        próbuje po nazwie i wersji.
        """
        try:
            dataset = fetch_openml(
                data_id=self.openml_data_id,
                as_frame=True,
                parser="auto"
            )
        except Exception:
            logger.warning("Pobieranie po data_id nie powiodło się. Próba pobrania po nazwie datasetu...")
            dataset = fetch_openml(
                name=self.dataset_name,
                version=self.dataset_version,
                as_frame=True,
                parser="auto"
            )

        raw_df = dataset.frame.copy()

        if "SalePrice" not in raw_df.columns and getattr(dataset, "target", None) is not None:
            raw_df["SalePrice"] = dataset.target

        return raw_df

    def _find_column(self, df: pd.DataFrame, possible_names: list[str]) -> str | None:
        """Szuka kolumny po kilku możliwych nazwach."""
        for name in possible_names:
            if name in df.columns:
                return name
        return None

    def _normalize_openml_house_prices(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Mapuje oryginalne kolumny Ames Housing Dataset na format używany przez aplikację.
        """
        neighborhood_col = self._find_column(raw_df, ["Neighborhood"])
        zoning_col = self._find_column(raw_df, ["MSZoning", "MS Zoning"])
        building_type_col = self._find_column(raw_df, ["BldgType", "Bldg Type"])
        house_style_col = self._find_column(raw_df, ["HouseStyle", "House Style"])
        area_col = self._find_column(raw_df, ["GrLivArea", "Gr Liv Area"])
        rooms_col = self._find_column(raw_df, ["TotRmsAbvGrd", "TotRms AbvGrd", "TotRms Abv Grd"])
        year_built_col = self._find_column(raw_df, ["YearBuilt", "Year Built"])
        price_col = self._find_column(raw_df, ["SalePrice", "Sale Price"])
        year_sold_col = self._find_column(raw_df, ["YrSold", "Yr Sold"])
        month_sold_col = self._find_column(raw_df, ["MoSold", "Mo Sold"])

        required_columns = {
            "Neighborhood": neighborhood_col,
            "GrLivArea": area_col,
            "YearBuilt": year_built_col,
            "SalePrice": price_col,
            "YrSold": year_sold_col,
            "MoSold": month_sold_col,
        }

        missing = [name for name, col in required_columns.items() if col is None]
        if missing:
            raise ValueError(f"Brakuje wymaganych kolumn w danych OpenML: {missing}")

        df = pd.DataFrame()

        neighborhood = raw_df[neighborhood_col].astype(str).str.strip()

        area_m2 = pd.to_numeric(raw_df[area_col], errors="coerce") * 0.092903
        rooms = pd.to_numeric(raw_df[rooms_col], errors="coerce") if rooms_col else 1
        year_built = pd.to_numeric(raw_df[year_built_col], errors="coerce")
        price = pd.to_numeric(raw_df[price_col], errors="coerce")

        year_sold = pd.to_numeric(raw_df[year_sold_col], errors="coerce").fillna(2010).astype(int)
        month_sold = pd.to_numeric(raw_df[month_sold_col], errors="coerce").fillna(1).astype(int)
        month_sold = month_sold.clip(lower=1, upper=12)

        date_added = pd.to_datetime(
            {
                "year": year_sold,
                "month": month_sold,
                "day": 1,
            },
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        if zoning_col:
            district = raw_df[zoning_col].astype(str).str.strip()
        else:
            district = neighborhood

        if building_type_col:
            property_type = raw_df[building_type_col].astype(str).str.strip()
        else:
            property_type = "House"

        if house_style_col:
            floor = self._map_house_style_to_floor(raw_df[house_style_col])
        else:
            floor = 1

        df["title"] = "House in " + neighborhood
        df["city"] = neighborhood
        df["district"] = district
        df["property_type"] = property_type
        df["area"] = area_m2.round(2)
        df["rooms"] = rooms
        df["floor"] = floor
        df["year_built"] = year_built
        df["price"] = price
        df["date_added"] = date_added

        return df.dropna(subset=["area", "price", "year_built"])

    def _map_house_style_to_floor(self, house_style_series: pd.Series) -> pd.Series:
        """Uproszczone mapowanie stylu domu na liczbę kondygnacji."""
        def map_value(value: object) -> int:
            text = str(value).lower()

            if "2" in text:
                return 2
            if "1.5" in text:
                return 1
            if "sfoyer" in text or "slvl" in text:
                return 1

            return 1

        return house_style_series.apply(map_value)

    def _generate_synthetic_data(self) -> pd.DataFrame:
        """
        Generator awaryjny, uruchamiany tylko wtedy, gdy nie uda się pobrać danych z internetu.
        """
        np.random.seed(42)

        records = 100
        locations = ["CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst"]
        property_types = ["1Fam", "TwnhsE", "Duplex"]

        data = {
            "title": [f"Test house offer {i}" for i in range(records)],
            "city": [np.random.choice(locations) for _ in range(records)],
            "district": [np.random.choice(["RL", "RM", "FV"]) for _ in range(records)],
            "property_type": [np.random.choice(property_types) for _ in range(records)],
            "area": np.random.randint(50, 220, size=records).astype(float),
            "rooms": np.random.randint(2, 9, size=records),
            "floor": np.random.randint(1, 3, size=records),
            "year_built": np.random.randint(1950, 2020, size=records),
            "price": np.random.randint(80000, 500000, size=records).astype(float),
            "date_added": ["2010-05-01" for _ in range(records)],
        }

        return pd.DataFrame(data)
