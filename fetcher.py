"""
Main module for data fetching.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from urllib.error import HTTPError
from contextlib import closing

from requests import get
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import chardet


class DataFetcher(ABC):
    """
        This is a base class for data fetching.

        Args:
            factory_date (datetime): The date for data fetching.

        Methods:
            fetch_data(): This method should be implemented by subclasses to fetch data.
    """

    def __init__(self, factory_date: datetime):
        self.factory_date = factory_date

    @abstractmethod
    def fetch_data(self):
        """
            This method should be implemented by subclasses to fetch data.
        """


class PSE5YearsPlanDataFetcher(DataFetcher):
    """
        A data fetcher for retrieving data from Polskie Sieci Energetyczne (PSE) -
        Polish Power System Operation - Coordinated 5-years Plan - Basic data.

        This class fetches data for a specific date range and returns it as a pandas DataFrame.

        Args:
            factory_date (datetime): The date for data fetching.

        Methods:
            fetch_data(): This method fetches data and returns a DataFrame.

        Raises:
            HTTPError: If there is an HTTP error while requesting data.
            pd.errors.ParserError: If there is an error parsing the CSV data.
    """

    def fetch_data(self):
        current_date = self.factory_date.strftime('%Y%m%d')
        next_date = (self.factory_date + timedelta(days=1)).strftime('%Y%m%d')

        url = f"https://www.pse.pl/getcsv/-/export/csv/PL_PD_GO_BILANS/data_od/{current_date}/" \
              f"data_do/{next_date}"
        try:
            data = pd.read_csv(url, encoding="ISO-8859-11", sep=";")
            # print(data['Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB'].head(24))
            data["Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB dost๊pna dla OSP"] = \
                data["Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB dost๊pna dla OSP"].str.replace('\xa0', '')
            data["Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB dost๊pna dla OSP"] = \
                pd.to_numeric( data["Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB dost๊pna dla OSP"], errors='coerce')
            data['Doba'] = pd.to_datetime(data['Doba'])
            data.set_index('Doba', inplace=True)
            return data.head(24)
        except HTTPError as e:
            raise ValueError(f"HTTP Error {e.code}: {e.reason}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV data: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"UnicodeDecodeError: {e}")


class PSEBalancingMarketFetcher(DataFetcher):
    """
        A data fetcher for retrieving data from Polskie Sieci Energetyczne (PSE) -
        Polish Power System Operation - Balancing Market Operation - Energy & Prices on Balancing Market data.

        This class fetches data for a specific date range and returns it as a pandas DataFrame.

        Args:
            factory_date (datetime): The date for data fetching.

        Methods:
            fetch_data(): This method fetches data and returns a DataFrame.

        Raises:
            HTTPError: If there is an HTTP error while requesting data.
            pd.errors.ParserError: If there is an error parsing the CSV data.
    """

    def fetch_data(self):
        date = self.factory_date.strftime('%Y%m%d')

        url = f"https://www.pse.pl/getcsv/-/export/csv/PL_CENY_NIEZB_RB/data/{date}"
        try:
            response = get(url, headers={'Range': 'bytes=0-1000'})
            content = response.content
            result = chardet.detect(content)
            encoding = result['encoding']

            data = pd.read_csv(url, encoding="ISO-8859-11", sep=";")
            data['Data'] = pd.to_datetime(data['Data'], format='%Y%m%d', errors='coerce')
            data.set_index('Data', inplace=True)
            data = data.apply(lambda col: col.str.replace(',', '.') if col.dtype == 'O' else col)
            return data
        except HTTPError as e:
            raise ValueError(f"HTTP Error {e.code}: {e.reason}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV data: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"UnicodeDecodeError: {e}")


class PSECurrentDailyCoordinationPlanFetcher(DataFetcher):
    """
        A data fetcher for retrieving data from Polskie Sieci Energetyczne (PSE) -
        Polish Power System Operation - Current Daily Coordination Plan - Basic data.

        This class fetches data for a specific date range and returns it as a pandas DataFrame.

        Args:
            factory_date (datetime): The date for data fetching.

        Methods:
            fetch_data(): This method fetches data and returns a DataFrame.

        Raises:
            HTTPError: If there is an HTTP error while requesting data.
            pd.errors.ParserError: If there is an error parsing the CSV data.
    """

    def fetch_data(self):
        date = self.factory_date.strftime('%Y%m%d')

        url = f"https://www.pse.pl/getcsv/-/export/csv/PL_BPKD/data/{date}"
        try:
            data = pd.read_csv(url, encoding="ISO-8859-11", sep=";")
            return data
        except HTTPError as e:
            raise ValueError(f"HTTP Error {e.code}: {e.reason}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV data: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"UnicodeDecodeError: {e}")


class DayAheadDataFetcher(DataFetcher):
    """
        A data fetcher for retrieving data from TGE (Polish Power Exchange) - Day-Ahead Market.

        This class fetches electricity price data from the TGE website for a specific date
        and returns it as a pandas DataFrame.

        Args:
            factory_date (datetime): The date for data fetching.

        Methods:
            fetch_data(): This method fetches electricity price data and returns it as a DataFrame.
    """

    def fetch_data(self):
        # Subtract 1 day from the date because the service provides data that is 1 day ahead."
        self.factory_date = self.factory_date - timedelta(days=1)
        url = f"https://www.tge.pl/energia-elektryczna-rdn?dateShosw=" \
              f"{self.factory_date.strftime('%d-%m-%Y')}&dateAction=next"
        # Recall the subtraction
        self.factory_date = self.factory_date + timedelta(days=1)

        def get_html(url):
            try:
                with closing(get(url, stream=False)) as resp:
                    if resp.status_code == 200 and resp.headers['content-type'] is not None:
                        return resp
                    else:
                        return None
            except ConnectionError as ce:
                raise ConnectionError(f"ConnectionError: {ce}")

        try:
            result = get_html(url)

            if result is not None:
                bs = BeautifulSoup(result.text, 'lxml')
                prices = []
                fixing = 1
                for index, body in enumerate(bs.find_all('tbody')):
                    if index == 2:
                        for index2, price in enumerate(body.find_all('td', 'footable-visible')):
                            if index2 == fixing:
                                prices.append(
                                    float([price.get_text().strip().replace(',', '.')][0]))
                                fixing += 7
                data = pd.DataFrame(data=prices, columns=['price'])
                data['date'] = self.factory_date.strftime('%Y-%m-%d')
                # Convert the 'date' column to datetime format
                data['date'] = pd.to_datetime(data['date'])

                # Set the 'date' column as the index
                data.set_index('date', inplace=True)
                data['hour'] = list(range(1, 25))
                return data
            else:
                # Raise an exception when the response is None
                raise ValueError("Error: Unable to retrieve data from the server.")
        except Exception as e:
            # Raise any other exceptions
            raise ValueError(f"An unexpected error occurred: {e}")


class IntraDayMarketFetcher(DataFetcher):
    """
    A data fetcher for retrieving data from TGE (Polish Power Exchange) - Intra Day Market.

    This class fetches electricity price data from the TGE website for a specific date
    and returns it as a pandas DataFrame.

    Args:
        factory_date (datetime): The date for data fetching.

    Methods:
        fetch_data(): This method fetches electricity price data and returns it as a DataFrame.
    """

    def fetch_data(self):
        avg = []
        for hour in range(1, 10):
            try:
                url = 'https://www.tge.pl/graph-days?targetId=IDM_{}_H0{}&dateStart={}&soapType=XBID&currency=pln&hour=max'.format(
                    self.factory_date.strftime('%d-%m-%y'),
                    hour,
                    self.factory_date.strftime('%Y-%m-%d'))
                r = get(url)
                data = pd.DataFrame(r.json()['data'])
                avg.append(np.average(data['kurs'], weights=data['volumen']))
            except Exception as e:
                avg.append(np.nan)
        for hour in range(10, 25):
            try:
                url = 'https://www.tge.pl/graph-days?targetId=IDM_{}_H{}&dateStart={}&soapType=XBID&currency=pln&hour=max'.format(
                    self.factory_date.strftime('%d-%m-%y'),
                    hour,
                    self.factory_date.strftime('%Y-%m-%d'))
                r = get(url)
                data = pd.DataFrame(r.json()['data'])
                avg.append(np.average(data['kurs'], weights=data['volumen']))
            except Exception as e:
                avg.append(np.nan)
        # Pobieranie danych z strony Rynku Dnia Bieżącego
        link = 'https://www.tge.pl/energia-elektryczna-rdb?dateShow={}&dateAction=prev'.format(
            self.factory_date.strftime('%d-%m-%Y'))

        def gethtml(url):
            try:
                with closing(get(url, stream=False)) as resp:
                    return resp
                    if resp.status_code == 200 and resp.headers['content-type'] is not None:
                        return resp
                    return None
            except Exception as e:
                print(e)
                # log_error('Error during requests to {0} : {1}'.format(url, str(e)))
                return None

        result = gethtml(link)

        bs = BeautifulSoup(result.text, 'lxml')
        body = []
        for link in bs.find_all('tbody'):
            body.append(link)

        headings = []
        for td in body[0].find_all('td'):
            # remove any newlines and extra spaces from left and right
            headings.append(td)

        r = 2
        temp = []
        for i in range(24):
            temp.append(str(headings[r]))
            r += 11
        rdb_min = []
        for i in range(24):
            rdb_min.append(temp[i].split('>')[2].split('<')[0].replace(',', '.'))

        r = 3
        temp = []
        for i in range(24):
            temp.append(str(headings[r]))
            r += 11
        rdb_max = []
        for i in range(24):
            rdb_max.append(temp[i].split('>')[2].split('<')[0].replace(',', '.'))
        r = 4
        temp = []
        for i in range(24):
            temp.append(str(headings[r]))
            r += 11
        rdb_avg = []
        for i in range(24):
            rdb_avg.append(temp[i].split('>')[2].split('<')[0].replace(',', '.'))

        data = pd.DataFrame([rdb_min, rdb_max, rdb_avg], index=['min', 'max', 'last'])
        data = data.transpose()
        data['date'] = self.factory_date.strftime('%Y-%m-%d')
        # Convert the 'date' column to datetime format
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.rename(columns={'min': 'cenaIntraMin', 'max': 'cenaIntraMax'}, inplace=True)
        data['cenaIntraAvg'] = avg
        data['hour'] = list(range(1, 25))
        return data[['cenaIntraAvg', 'cenaIntraMin', 'cenaIntraMax', 'hour']]

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
        if source == "PSE 5-years Plan":
            return PSE5YearsPlanDataFetcher(factory_date)
        if source == "PSE Balancing Market":
            return PSEBalancingMarketFetcher(factory_date)
        if source == "PSE Current Daily Coordination Plan":
            return PSECurrentDailyCoordinationPlanFetcher(factory_date)
        if source == "Day-Ahead":
            return DayAheadDataFetcher(factory_date)
        if source == "Intra-Day":
            return IntraDayMarketFetcher(factory_date)
        else:
            raise ValueError("Invalid source specified")


if __name__ == "__main__":
    date = datetime(2023, 12, 27)
    # Example usage:
    data_fetcher_factory = DataFetcherFactory()
    try:
        # Create a PSE data fetcher
        pse_5_fetcher = data_fetcher_factory.create_data_fetcher("PSE 5-years Plan", date)
        print(pse_5_fetcher.fetch_data())
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")

    try:
        # Create a PSE data fetcher
        pse_bal_fetcher = data_fetcher_factory.create_data_fetcher("PSE Balancing Market", date)
        print(pse_bal_fetcher.fetch_data())
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")

    try:
        # Create a PSE data fetcher
        pse_bal_fetcher = data_fetcher_factory.create_data_fetcher(
            "PSE Current Daily Coordination Plan", date)
        print(pse_bal_fetcher.fetch_data())
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")

    try:
        # Create a TGE data fetcher
        tge_fetcher = data_fetcher_factory.create_data_fetcher("Day-Ahead", date)
        print(tge_fetcher.fetch_data())
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")
    try:
        # Create a TGE data fetcher
        tge_fetcher = data_fetcher_factory.create_data_fetcher("Intra-Day", date)
        print(tge_fetcher.fetch_data())
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")
