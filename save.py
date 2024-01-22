from datetime import datetime, timedelta
import sqlite3

import numpy as np
import pandas as pd

from database import Database
from fetcher import DataFetcherFactory


def fetch_data(date: datetime, name: str) -> DataFetcherFactory:
    """
    Fetches data using a DataFetcherFactory based on the specified date and name.

    Args:
        date (datetime): The date for which to fetch the data.
        name (str): The name of the data source.

    Returns:
        pd.DataFrame: A DataFrame containing data from the specified source and date.

    Raises:
        ValueError: If there is an error creating the data fetcher.
    """
    try:
        data_fetcher_factory = DataFetcherFactory()
        fetcher = data_fetcher_factory.create_data_fetcher(name, date)
        return fetcher.fetch_data()
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")


def insert_date(db: Database, data: pd.DataFrame):
    """
   Inserts date information into the database.

   Args:
       db (Database): The database instance.
       data (pd.DataFrame): The DataFrame containing date information.

   Prints:
       Status messages regarding the success or failure of the operation.
   """
    query = insert_date_query = f"INSERT INTO date (date_value) " \
                                f"VALUES ('{data.index[0].strftime('%Y-%m-%d')}')"
    try:
        db.insert_data(query)
        print(f"Date {data.index[0].strftime('%Y-%m-%d')} save correctly")
    except sqlite3.IntegrityError:
        print(f"Date: {data.index[0].strftime('%Y-%m-%d')} already exist in Date table")


def insert_day_ahead(db: Database, data: pd.DataFrame):
    """
    Inserts Day Ahead data into the database.

    Args:
        db (Database): The database instance.
        data (pd.DataFrame): The DataFrame containing Day Ahead data.

    Prints:
        Status messages regarding the success or failure of the operation.
    """
    query = f"SELECT date_id " \
            f"FROM date " \
            f"WHERE date_value = '{df_da.index[0].strftime('%Y-%m-%d')}'"
    date = db.select_data(query)
    date_id = date[0][0]
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT INTO day_ahead (hour_of_day, date_id, price) " \
                           f"VALUES ('{row['hour']}', {date_id}, {row['price']})"
            db.insert_data(insert_query)
        print("Data from Day Ahead saved correctly.")
    except sqlite3.IntegrityError:
        print(f"Date: {data.index[0].strftime('%Y-%m-%d')} already exist in Day Ahead table")


def insert_intra(db: Database, data: pd.DataFrame):
    """
    Inserts Intra Day data into the database.

    Args:
        db (Database): The database instance.
        data (pd.DataFrame): The DataFrame containing Intra Day data.

    Prints:
        Status messages regarding the success or failure of the operation.
    """
    query = f"SELECT date_id " \
            f"FROM date " \
            f"WHERE date_value = '{data.index[0].strftime('%Y-%m-%d')}'"
    date = db.select_data(query)
    date_id = date[0][0]
    print(data)
    data.replace('-', "Null", inplace=True)
    data.replace(np.nan, "Null", inplace=True)
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT INTO intra_day (hour_of_day, date_id, intraday_avg_price, intraday_min_price, intraday_max_price) " \
                           f"VALUES ('{row['hour']}', {date_id}, {row['cenaIntraAvg']}, {row['cenaIntraMin']}, {row['cenaIntraMax']})"
            DB.insert_data(insert_query)
        print("Data from Intra Day saved correctly.")
    except sqlite3.IntegrityError:
        print(f"Date: {df_intra.index[0].strftime('%Y-%m-%d')} already exist in Intra Day table")


def insert_pse_5(db: Database, data: pd.DataFrame):
    pass


def insert_pse_bal(db: Database, data: pd.DataFrame):
    pass


def insert_pse_current(db: Database, data: pd.DataFrame):
    pass


if __name__ == "__main__":
    DATE = datetime.now()
    DB = Database("energy.db")
    SQLITE_PATH = 'energy.db'

    # Day Ahead
    df_da = fetch_data(DATE, "Day-Ahead")
    # Save date which was fetched from Day Ahead
    insert_date(DB, df_da)
    # Save data which was fetched from Day Ahead
    insert_day_ahead(DB, df_da)

    # Intra Day
    df_intra = fetch_data(DATE, "Intra-Day")
    # Save date which was fetched from Intra Day
    insert_date(DB, df_intra)
    # Save data which was fetched from Intra Day
    insert_intra(DB, df_intra)
