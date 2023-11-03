"""
Main module for data fetching.
"""
from datetime import datetime, timedelta
from urllib.error import HTTPError

import pandas as pd

class DataFetcher:
    def __init__(self, factory_date: datetime):
        self.factory_date = factory_date

    def fetch_data(self):
        pass


class PSEDataFetcher(DataFetcher):
    def fetch_data(self):
        """
        Fetches data from Polskie Sieci Energetyczne (PSE) for a specific date range.

        Returns:
            DataFrame: A pandas DataFrame containing the fetched data.

        Raises:
            HTTPError: If there is an HTTP error while requesting data.
            pd.errors.ParserError: If there is an error parsing the CSV data.
        """
        current_date = self.factory_date.strftime('%Y%m%d')
        next_date = (self.factory_date + timedelta(days=1)).strftime('%Y%m%d')

        url = f"https://www.pse.pl/getcsv/-/export/csv/PL_PD_GO_BILANS/data_od/{current_date}/data_do/{next_date}"

        try:
            data = pd.read_csv(url, encoding="cp1252", sep=";")
            return data
        except HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV data: {e}")
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")


class TGEDataFetcher(DataFetcher):
    def fetch_data(self):
        # Implement the data fetching logic for TGE here
        print(f"Fetching data from Towarowa Giełda Energii (TGE): {self.factory_date.strftime('%Y-%m-%d')}")


class DataFetcherFactory:
    """
    Factory for creating data fetchers for different sources and dates.
    """

    def create_data_fetcher(self, source: str, factory_date: datetime):
        """
        Create a data fetcher for the specified source and date.

        Args:
            source (str): The data source (e.g., "PSE" or "TGE").
            factory_date (datetime): The date for data fetching.

        Returns:
            DataFetcher: An instance of the appropriate data fetcher class.

        Raises:
            ValueError: If an invalid source is specified.
        """
        if source == "PSE":
            return PSEDataFetcher(factory_date)
        elif source == "TGE":
            return TGEDataFetcher(factory_date)
        else:
            raise ValueError("Invalid source specified")


if __name__ == "__main__":
    date = datetime(2023, 10, 31)
    # Example usage:
    data_fetcher_factory = DataFetcherFactory()

    # Create a PSE data fetcher
    pse_fetcher = data_fetcher_factory.create_data_fetcher("PSE", date)
    print(pse_fetcher.fetch_data())

    # Create a TGE data fetcher
    tge_fetcher = data_fetcher_factory.create_data_fetcher("TGE", date)
    tge_fetcher.fetch_data()
