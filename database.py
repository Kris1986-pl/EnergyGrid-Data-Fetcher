import sqlite3


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def insert_data(self, sql: str):
        self.cursor.execute(sql)
        self.connection.commit()

    def select_data(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_data_by_date(self, sql: str, date: str):
        self.cursor.execute(sql, (date,))
        return self.cursor.fetchall()
