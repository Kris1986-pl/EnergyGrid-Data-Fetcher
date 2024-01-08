from datetime import datetime, timedelta
import sqlite3

import pandas as pd

from database import Database
from fetcher import DataFetcherFactory


def fetch_data(date: datetime, name: str) -> DataFetcherFactory:
    try:
        # Create a Day-Ahead data fetcher
        data_fetcher_factory = DataFetcherFactory()
        fetcher = data_fetcher_factory.create_data_fetcher(name, date)
        return fetcher.fetch_data()
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")


def insert_date(db: Database, data: pd.DataFrame):
    query = insert_date_query = f"INSERT INTO date (date_value) " \
                                f"VALUES ('{df_da.index[0].strftime('%Y-%m-%d')}')"
    try:
        db.insert_data(query)
        print(f"Date {data.index[0].strftime('%Y-%m-%d')} save correctly")
    except sqlite3.IntegrityError:
        print(f"Date: {data.index[0].strftime('%Y-%m-%d')} already exist in Date table")


def insert_day_ahead(db: Database, data: pd.DataFrame):
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


if __name__ == "__main__":
    DATE = datetime.now()
    DB = Database("energy.db")
    SQLITE_PATH = 'energy.db'

    # Day Ahead
    # Save date wihich was fetched from Day Ahead
    df_da = fetch_data(DATE, "Day-Ahead")
    insert_date(DB, df_da)
    # Save date which was fetched from Day Ahead
    insert_day_ahead(DB, df_da)

    # # Intra Day
    # df_intra = fetch_data(DATE, "Intra-Day")
    # print(df_intra)
