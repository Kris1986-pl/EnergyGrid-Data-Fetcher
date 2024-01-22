from datetime import datetime
import sqlite3

from database import Database
from fetcher import DataFetcherFactory


def fetch_day_ahead(date):
    try:
        # Create a Day-Ahead data fetcher
        data_fetcher_factory = DataFetcherFactory()
        fetcher = data_fetcher_factory.create_data_fetcher("Day-Ahead", date)
        return fetcher.fetch_data()
    except ValueError as ve:
        # Handle other ValueErrors
        print(f"Error: {ve}")


def insert_date(DB, df):
    try:
        DB.insert_data(insert_date_query)
    except sqlite3.IntegrityError:
        print(f"Date: {df.index[0].strftime('%Y-%m-%d')} already exist in Date table")


def insert_day_ahead(db, df, select_date_query):
    date = db.select_data(select_date_query)
    date_id = date[0][0]
    try:
        for index, row in df.iterrows():
            insert_query = f"INSERT INTO day_ahead (hour_of_day, date_id, price) VALUES ('{row['hour']}', {date_id}, {row['price']})"
            db.insert_data(insert_query)
    except sqlite3.IntegrityError:
        print(f"Date: {df.index[0].strftime('%Y-%m-%d')} already exist in Day Ahead table")


if __name__ == "__main__":
    DATE = datetime.now()
    DB = Database("energy.db")
    SQLITE_PATH = 'energy.db'

    df = fetch_day_ahead(DATE)
    insert_date_query = f"INSERT INTO date (date_value) VALUES ('{df.index[0].strftime('%Y-%m-%d')}')"
    insert_date(DB, df)

    select_date_query = f"SELECT date_id FROM date WHERE date_value = '{df.index[0].strftime('%Y-%m-%d')}'"
    insert_day_ahead(DB, df, select_date_query)
