from datetime import datetime, timedelta
import sqlite3

import numpy as np
import pandas as pd

from database import Database
from fetcher import DataFetcherFactory, ServicesEnergy


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
    data.replace('-', "Null", inplace=True)
    data.replace(np.nan, "Null", inplace=True)
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT OR REPLACE INTO intra_day " \
                           f"(hour_of_day, " \
                           f"date_id, " \
                           f"intraday_avg_price, " \
                           f"intraday_min_price, " \
                           f"intraday_max_price) " \
                           f"VALUES ('{row['hour']}', " \
                           f"{date_id}, " \
                           f"{row['cenaIntraAvg']}, " \
                           f"{row['cenaIntraMin']}, " \
                           f"{row['cenaIntraMax']})"
            DB.insert_data(insert_query)
        print("Data from Intra Day saved correctly.")
    except sqlite3.IntegrityError:
        print(f"Date: {data.index[0].strftime('%Y-%m-%d')} already exist in Intra Day table")


def insert_pse_5(db: Database, data: pd.DataFrame):
    """
        Inserts PSE (Polish Power Exchange) five-years plan data into the database.

        Args:
            db (Database): The database instance.
            data (pd.DataFrame): The DataFrame containing PSE five-years plan data.

        Prints:
            Status messages regarding the success or failure of the operation.
        """
    query = f"SELECT date_id " \
            f"FROM date " \
            f"WHERE date_value = '{data.index[0].strftime('%Y-%m-%d')}'"
    date = db.select_data(query)
    date_id = date[0][0]
    data.replace('-', "Null", inplace=True)
    data.replace(np.nan, "Null", inplace=True)
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT INTO five_years_plan (hour_of_day, " \
                           f"date_id, GridDemandForecast, " \
                           f"RequiredPowerReserve, " \
                           f"SurplusCapacityAvailableForTSO, " \
                           f"GenerationCapacitySurplusForTSO, " \
                           f"AvailableCapacityBalancingMarketUnits, " \
                           f"AvailableForTSOCapacityBalancingMarketUnits, " \
                           f"PredictedGenerationBalancingMarket, " \
                           f"ForecastedGenerationNonBalancingMarket, " \
                           f"WindTotalGenerationForecast, " \
                           f"PhotovoltaicTotalGenerationForecast, " \
                           f"PlannedCrossBorderElectricityExchange, " \
                           f"ForecastedUnavailabilityTransmissionAndDistribution, " \
                           f"GenerationCapacityUnavailabilityThermalUnitsBalancingMarket, " \
                           f"PredictedGenerationNonCoveredByCapacityMarketObligation, " \
                           f"CapacityMarketObligationAllUnits) " \
                           f"VALUES ('{row['Godzina']}', " \
                           f"{date_id}, " \
                           f"{row['Prognozowane zapotrzebowanie sieci']}, " \
                           f"{row['Wymagana rezerwa mocy OSP']}, " \
                           f"{row['Nadwyฟka mocy dost๊pna dla OSP (8) + (10) - [(3)-(13)]-(14)']}, " \
                           f"{row['Nadwyฟka mocy dost๊pna dla OSP ponad wymaganน rezerw๊ moc (5) - (4)']}, " \
                           f"{row['Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB']}, " \
                           f"{row['Moc dyspozycyjna JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB dost๊pna dla OSP']}, " \
                           f"{row['Przewidywana generacja JW i magazyn๓w energii wiadczนcych usณugi bilansujนce w ramach RB (3) - (10) - (13)']}, " \
                           f"{row['Prognozowana generacja JW i magazyn๓w energii nie wiadczนcych usณug bilansujนcych w ramach RB']}, " \
                           f"{row['Prognozowana sumaryczna generacja r๓deณ wiatrowych']}, " \
                           f"{row['Prognozowana sumaryczna generacja r๓deณ fotowoltaicznych']}, " \
                           f"{row['Planowane saldo wymiany mi๊dzysystemowej']}, " \
                           f"{row['Prognozowana wielkoๆ niedyspozycyjnoci wynikajนca z ogranicze๑ sieciowych wyst๊pujนcych w sieci przesyณowej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej']}, " \
                           f"{row['Prognozowana wielkoๆ niedyspozycyjnoci wynikajนcych z warunk๓w eksploatacyjnych JW wiadczนcych usณugi bilansujนce w ramach RB']}, " \
                           f"{row['Przewidywana generacja zasob๓w wytw๓rczych nieobj๊tych obowiนzkami mocowymi']}, " \
                           f"{row['Obowiนzki mocowe wszystkich jednostek rynku mocy']})"
            DB.insert_data(insert_query)
        print("Data from PSE five-years plan saved correctly.")
    except sqlite3.IntegrityError:
        print(
            f"Date: {data.index[0].strftime('%Y-%m-%d')} already exist in PSE five-years plan table")


def insert_pse_bal(db: Database, data: pd.DataFrame):
    query = f"SELECT date_id " \
            f"FROM date " \
            f"WHERE date_value = '{data.index[0].strftime('%Y-%m-%d')}'"
    date = db.select_data(query)
    date_id = date[0][0]
    data.replace('-', "Null", inplace=True)
    data.replace(np.nan, "Null", inplace=True)
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT OR REPLACE INTO balancing_market (hour_of_day, " \
                           f"date_id, " \
                           f"CRO, " \
                           f"CROs, " \
                           f"CROz, " \
                           f"AggregatedMarketParticipantsContractingStatus, " \
                           f"Imbalance) " \
                           f"VALUES ({row['Godzina']}, " \
                           f"{date_id}, " \
                           f"{row['CRO']}, " \
                           f"{row['CROs']}, " \
                           f"{row['CROz']}, " \
                           f"{row['Stan zakontraktowania']}, " \
                           f"{row['Niezbilansowanie']})"
            DB.insert_data(insert_query)
        print("Data from PSE Balancing Market saved correctly.")
    except sqlite3.DatabaseError as e:
        print(e)


def insert_pse_current(db: Database, data: pd.DataFrame):
    query = f"SELECT date_id " \
            f"FROM date " \
            f"WHERE date_value = '{data.index[0].strftime('%Y-%m-%d')}'"
    date = db.select_data(query)
    date_id = date[0][0]
    data.replace('-', "Null", inplace=True)
    data.replace(np.nan, "Null", inplace=True)
    # print(data.columns)
    try:
        for index, row in data.iterrows():
            insert_query = f"INSERT OR REPLACE INTO current_daily_plan " \
                           f"(hour_of_day, " \
                           f"date_id, " \
                           f"NationalPowerDemand," \
                           f"TotalProductionCapacity_KSE," \
                           f"TotalProductionCapacity_JGWa," \
                           f"TotalProductionCapacity_JGFWa," \
                           f"TotalProductionCapacity_JGMa," \
                           f"TotalProductionCapacity_JGPVa," \
                           f"TotalGeneration_ActiveJG," \
                           f"TotalGeneration_JGWa," \
                           f"TotalGeneration_JGFWa," \
                           f"TotalGeneration_JGMa," \
                           f"TotalGeneration_JGPVa," \
                           f"TotalGeneration_NonParticipatingUnits," \
                           f"WindPowerGeneration," \
                           f"PVPowerGeneration," \
                           f"TotalChargingCapacity_JGMa," \
                           f"NationalParallelExchangeBalance," \
                           f"NationalNonParallelExchangeBalance," \
                           f"ExcessCapacityAboveDemand," \
                           f"ExcessCapacityBelowDemand," \
                           f"TotalCapacityFromUtilizedLoadReductionOffers_JGOa)" \
                           f"VALUES ({row['Godzina']}, " \
                           f"{date_id}, " \
                           f"{row['Krajowe zapotrzebowanie na moc']}, " \
                           f"{row['Suma zdolnoci wytw๓rczych jednostek wytw๓rczych w KSE']}, " \
                           f"{row['Suma zdolnoci wytw๓rczych JGWa']}, " \
                           f"{row['Suma zdolnoci wytw๓rczych JGFWa']}, " \
                           f"{row['Suma zdolnoci wytw๓rczych JGMa']}, " \
                           f"{row['Suma zdolnoci wytw๓rczych JGPVa']}, " \
                           f"{row['Sumaryczna generacja JG aktywnych: JGWa, JGFWa, JGMa i JGPVa']}, " \
                           f"{row['Sumaryczna generacja JGWa']}," \
                           f"{row['Sumaryczna generacja JGFWa']}, " \
                           f"{row['Sumaryczna generacja JGMa']}, " \
                           f"{row['Sumaryczna generacja JGPVa']}, " \
                           f"{row['Sumaryczna generacja jednostek wytw๓rczych nieuczestniczนcych aktywnie w Rynku Bilansujนcym']}, " \
                           f"{row['Generacja r๓deณ wiatrowych']}, " \
                           f"{row['Generacja r๓deณ fotowoltaicznych']}, " \
                           f"{row['Sumaryczna moc ณadowania JGMa']}, " \
                           f"{row['Krajowe saldo wymiany mi๊dzysystemowej r๓wnolegณej']}, " \
                           f"{row['Krajowe saldo wymiany mi๊dzysystemowej nier๓wnolegณej']}, " \
                           f"{row['Rezerwa mocy ponad zapotrzebowanie']}, " \
                           f"{row['Rezerwa mocy poniฟej zapotrzebowania']}, " \
                           f"{row['Suma mocy z wykorzystanych Ofert Redukcji Obciนฟenia JGOa']})"
            # print(insert_query)
            DB.insert_data(insert_query)
        print("Data from PSE Current Daily Coordination Plan saved correctly.")
    except sqlite3.DatabaseError as e:
        print(e)


if __name__ == "__main__":
    DATE = datetime.now()
    DB = Database("energy.db")
    SQLITE_PATH = 'energy.db'

    # Day Ahead
    print("Day Ahead is being fetched...")
    df_da = fetch_data(DATE, ServicesEnergy.DAY_AHEAD)
    # Save date which was fetched from Day Ahead
    insert_date(DB, df_da)
    # Save data which was fetched from Day Ahead
    insert_day_ahead(DB, df_da)

    # Intra Day
    print("Intra Day is being fetched...")
    df_intra = fetch_data(DATE, ServicesEnergy.INTRA_DAY)
    # Save date which was fetched from Intra Day
    insert_date(DB, df_intra)
    # Save data which was fetched from Intra Day
    insert_intra(DB, df_intra)

    # PSE 5-years Plan
    print("PSE 5-years Plan is being fetched...")
    df_pse_5 = fetch_data(DATE, ServicesEnergy.PSE_5_YEARS_PLAN)
    # Save date which was fetched from PSE 5-years Plan
    insert_date(DB, df_pse_5)
    # Save data which was fetched from PSE 5-years Plan
    insert_pse_5(DB, df_pse_5)

    # PSE PSE Balancing Market
    print("PSE Balancing Market is being fetched...")
    df_bal = fetch_data(DATE, ServicesEnergy.PSE_BALANCING_MARKET)
    # Save date which was fetched from PSE Balancing Market
    insert_date(DB, df_bal)
    # Save data which was fetched from PSE Balancing Market
    insert_pse_bal(DB, df_bal)

    # PSE Current Daily
    print("PSE Current Daily Coordination Plan is being fetched...")
    df_curr = fetch_data(DATE, ServicesEnergy.PSE_CURRENT_DAILY_COORDINATION_PLAN)
    # Save date which was fetched from PSE Balancing Market
    insert_date(DB, df_curr)
    # Save data which was fetched from PSE Balancing Market
    insert_pse_current(DB, df_curr)
