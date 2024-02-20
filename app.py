from flask import Flask, g, jsonify
from flask_cors import CORS
import sqlite3
import json
from database import Database

app = Flask(__name__)
CORS(app)
DATABASE = 'energy.db'


def get_db() -> Database:
    """
   Retrieve the database connection from the Flask application context.

   Returns:
   Database: The database connection.
   """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database(DATABASE)
    return db


# Add your setup_command function here to create tables

def fetch_data_endpoint(query: str, endpoint_name: str, key_names: list[str]) -> jsonify:
    """
   Fetch data from the database based on the provided query and organize it by date.

   Args:
   query (str): SQL query to fetch data.
   endpoint_name (str): Name of the endpoint.
   key_names (list[str]): List of key names for the records.

   Returns:
   jsonify: Flask JSON response containing the organized data.
   """
    db = get_db()
    results = db.select_data(query)

    # Organize the data by date
    data_by_date = {}
    for result in results:
        date_key = result[1]
        record = {key_names[i]: result[i] for i in range(len(key_names)) if
                  key_names[i] is not "date"}
        if date_key in data_by_date:
            data_by_date[date_key].append(record)
        else:
            data_by_date[date_key] = [record]

    # Convert the dictionary to a list of dictionaries
    data = [{'date': date, 'records': records} for date, records in data_by_date.items()]

    # Use json.dumps with sort_keys parameter
    ordered_json_data = json.dumps({f'{endpoint_name}_data': data}, sort_keys=False)

    # Set the content type to 'application/json'
    response = jsonify(json.loads(ordered_json_data))
    response.headers['Content-Type'] = 'application/json'

    return response


def fetch_data_endpoint_by_date(query: str, endpoint_name: str, key_names: list[str],
                                date: str) -> jsonify:
    """
    Fetch data from the database based on the provided query, organize it by date,
    and filter by a specific date.

    Args:
    query (str): SQL query to fetch data.
    endpoint_name (str): Name of the endpoint.
    key_names (list[str]): List of key names for the records.
    date (str): Date to filter the results.

    Returns:
    jsonify: Flask JSON response containing the organized data for the specified date.
    """
    db = get_db()
    results = db.select_data_by_date(query, date)

    # Organize the data by date
    data_by_date = {}
    for result in results:
        date_key = result[1]
        record = {key_names[i]: result[i] for i in range(len(key_names)) if
                  key_names[i] is not "date"}
        if date_key in data_by_date:
            data_by_date[date_key].append(record)
        else:
            data_by_date[date_key] = [record]

    # Convert the dictionary to a list of dictionaries
    data = [{'date': date, 'records': records} for date, records in data_by_date.items()]

    # Use json.dumps with sort_keys parameter
    ordered_json_data = json.dumps({f'{endpoint_name}_data': data}, sort_keys=False)

    # Set the content type to 'application/json'
    response = jsonify(json.loads(ordered_json_data))
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route("/days-ahead")
def fetch_days_ahead():
    query = "SELECT day_ahead_id, date_value, hour_of_day, price " \
            "FROM day_ahead " \
            "INNER JOIN date ON date.date_id = day_ahead.date_id"
    return fetch_data_endpoint(query, 'days_head',
                               ['id', 'date', 'hour', 'price'])


@app.route("/intra-days")
def fetch_intra_days():
    query = "SELECT intra_day_id, date_value, hour_of_day, " \
            "intraday_avg_price, intraday_min_price, intraday_max_price " \
            "FROM intra_day " \
            "INNER JOIN date ON date.date_id = intra_day.date_id"
    return fetch_data_endpoint(query, 'intra_day',
                               ['id', 'date', 'hour', 'avg_price', 'min_price', 'max_price'])


@app.route("/current-daily-plans")
def fetch_current_daily_plans():
    query = "SELECT current_daily_plan_id, date_value, hour_of_day, " \
            "NationalPowerDemand, TotalProductionCapacity_KSE, TotalProductionCapacity_JGWa, " \
            "TotalProductionCapacity_JGFWa, TotalProductionCapacity_JGMa, TotalProductionCapacity_JGPVa, " \
            "TotalGeneration_ActiveJG, TotalGeneration_JGWa, TotalGeneration_JGFWa, TotalGeneration_JGMa, " \
            "TotalGeneration_JGPVa, TotalGeneration_NonParticipatingUnits, WindPowerGeneration, PVPowerGeneration, " \
            "TotalChargingCapacity_JGMa, NationalParallelExchangeBalance, NationalNonParallelExchangeBalance, " \
            "ExcessCapacityAboveDemand, ExcessCapacityBelowDemand, TotalCapacityFromUtilizedLoadReductionOffers_JGOa " \
            "FROM current_daily_plan " \
            "INNER JOIN date ON date.date_id = current_daily_plan.date_id"
    return fetch_data_endpoint(query, 'current_daily_plan',
                               ['id', 'date', 'hour', 'NationalPowerDemand',
                                'TotalProductionCapacity_KSE', 'TotalProductionCapacity_JGWa',
                                'TotalProductionCapacity_JGFWa', 'TotalProductionCapacity_JGMa',
                                'TotalProductionCapacity_JGPVa', 'TotalGeneration_ActiveJG',
                                'TotalGeneration_JGWa', 'TotalGeneration_JGFWa',
                                'TotalGeneration_JGMa', 'TotalGeneration_JGPVa',
                                'TotalGeneration_NonParticipatingUnits', 'WindPowerGeneration',
                                'PVPowerGeneration', 'TotalChargingCapacity_JGMa',
                                'NationalParallelExchangeBalance',
                                'NationalNonParallelExchangeBalance',
                                'ExcessCapacityAboveDemand', 'ExcessCapacityBelowDemand',
                                'TotalCapacityFromUtilizedLoadReductionOffers_JGOa'])


@app.route("/balancing-markets")
def fetch_balancing_markets():
    query = "SELECT balancing_market_id, date_value, hour_of_day, " \
            "CRO, CROs, CROz, AggregatedMarketParticipantsContractingStatus, Imbalance " \
            "FROM balancing_market " \
            "INNER JOIN date ON date.date_id = balancing_market.date_id"
    return fetch_data_endpoint(query, 'balancing_market',
                               ['id', 'date', 'hour', 'CRO', 'CROs', 'CROz',
                                'AggregatedMarketParticipantsContractingStatus', 'Imbalance'])


@app.route("/five-years-plans")
def fetch_five_years_plans():
    query = "SELECT five_years_plan_id, date_value, hour_of_day, " \
            "GridDemandForecast, RequiredPowerReserve, SurplusCapacityAvailableForTSO, " \
            "GenerationCapacitySurplusForTSO, AvailableCapacityBalancingMarketUnits, " \
            "AvailableForTSOCapacityBalancingMarketUnits, PredictedGenerationBalancingMarket, " \
            "ForecastedGenerationNonBalancingMarket, WindTotalGenerationForecast, " \
            "PhotovoltaicTotalGenerationForecast, PlannedCrossBorderElectricityExchange, " \
            "ForecastedUnavailabilityTransmissionAndDistribution, " \
            "GenerationCapacityUnavailabilityThermalUnitsBalancingMarket, " \
            "PredictedGenerationNonCoveredByCapacityMarketObligation, CapacityMarketObligationAllUnits " \
            "FROM five_years_plan " \
            "INNER JOIN date ON date.date_id = five_years_plan.date_id"
    return fetch_data_endpoint(query, 'five_years_plan',
                               ['id', 'date', 'hour', 'GridDemandForecast',
                                'RequiredPowerReserve', 'SurplusCapacityAvailableForTSO',
                                'GenerationCapacitySurplusForTSO',
                                'AvailableCapacityBalancingMarketUnits',
                                'AvailableForTSOCapacityBalancingMarketUnits',
                                'PredictedGenerationBalancingMarket',
                                'ForecastedGenerationNonBalancingMarket',
                                'WindTotalGenerationForecast',
                                'PhotovoltaicTotalGenerationForecast',
                                'PlannedCrossBorderElectricityExchange',
                                'ForecastedUnavailabilityTransmissionAndDistribution',
                                'GenerationCapacityUnavailabilityThermalUnitsBalancingMarket',
                                'PredictedGenerationNonCoveredByCapacityMarketObligation',
                                'CapacityMarketObligationAllUnits'])


@app.route("/days-ahead/<date>")
def fetch_days_ahead_by_date(date):
    query = "SELECT day_ahead_id, date_value, hour_of_day, price " \
            "FROM day_ahead " \
            "INNER JOIN date ON date.date_id = day_ahead.date_id " \
            "WHERE date_value = ?"
    return fetch_data_endpoint_by_date(query, 'day_ahead', ['id', 'date', 'hour', 'price'], date)


@app.route("/intra-days/<date>")
def fetch_intra_days_by_date(date):
    query = "SELECT intra_day_id, date_value, hour_of_day, " \
            "intraday_avg_price, intraday_min_price, intraday_max_price " \
            "FROM intra_day " \
            "INNER JOIN date ON date.date_id = intra_day.date_id " \
            "WHERE date_value = ?"
    return fetch_data_endpoint_by_date(query, 'intra_day',
                                       ['id', 'date', 'hour', 'avg_price', 'min_price',
                                        'max_price'], date)


@app.route("/current-daily-plans/<date>")
def fetch_current_daily_plans_by_date(date):
    query = "SELECT current_daily_plan_id, date_value, hour_of_day, " \
            "NationalPowerDemand, TotalProductionCapacity_KSE, TotalProductionCapacity_JGWa, " \
            "TotalProductionCapacity_JGFWa, TotalProductionCapacity_JGMa, TotalProductionCapacity_JGPVa, " \
            "TotalGeneration_ActiveJG, TotalGeneration_JGWa, TotalGeneration_JGFWa, TotalGeneration_JGMa, " \
            "TotalGeneration_JGPVa, TotalGeneration_NonParticipatingUnits, WindPowerGeneration, PVPowerGeneration, " \
            "TotalChargingCapacity_JGMa, NationalParallelExchangeBalance, NationalNonParallelExchangeBalance, " \
            "ExcessCapacityAboveDemand, ExcessCapacityBelowDemand, TotalCapacityFromUtilizedLoadReductionOffers_JGOa " \
            "FROM current_daily_plan " \
            "INNER JOIN date ON date.date_id = current_daily_plan.date_id " \
            "WHERE date_value = ?"
    return fetch_data_endpoint_by_date(query, 'current_daily_plan',
                                       ['id', 'date', 'hour', 'NationalPowerDemand',
                                        'TotalProductionCapacity_KSE',
                                        'TotalProductionCapacity_JGWa',
                                        'TotalProductionCapacity_JGFWa',
                                        'TotalProductionCapacity_JGMa',
                                        'TotalProductionCapacity_JGPVa', 'TotalGeneration_ActiveJG',
                                        'TotalGeneration_JGWa', 'TotalGeneration_JGFWa',
                                        'TotalGeneration_JGMa', 'TotalGeneration_JGPVa',
                                        'TotalGeneration_NonParticipatingUnits',
                                        'WindPowerGeneration',
                                        'PVPowerGeneration', 'TotalChargingCapacity_JGMa',
                                        'NationalParallelExchangeBalance',
                                        'NationalNonParallelExchangeBalance',
                                        'ExcessCapacityAboveDemand', 'ExcessCapacityBelowDemand',
                                        'TotalCapacityFromUtilizedLoadReductionOffers_JGOa'], date)


@app.route("/balancing-markets/<date>")
def fetch_balancing_markets_by_date(date):
    query = "SELECT balancing_market_id, date_value, hour_of_day, " \
            "CRO, CROs, CROz, AggregatedMarketParticipantsContractingStatus, Imbalance " \
            "FROM balancing_market " \
            "INNER JOIN date ON date.date_id = balancing_market.date_id " \
            "WHERE date_value = ?"
    return fetch_data_endpoint_by_date(query, 'balancing_market',
                                       ['id', 'date', 'hour', 'CRO', 'CROs', 'CROz',
                                        'AggregatedMarketParticipantsContractingStatus',
                                        'Imbalance'], date)


@app.route("/five-years-plans/<date>")
def fetch_five_years_plans_by_date(date):
    query = "SELECT five_years_plan_id, date_value, hour_of_day, " \
            "GridDemandForecast, RequiredPowerReserve, SurplusCapacityAvailableForTSO, " \
            "GenerationCapacitySurplusForTSO, AvailableCapacityBalancingMarketUnits, " \
            "AvailableForTSOCapacityBalancingMarketUnits, PredictedGenerationBalancingMarket, " \
            "ForecastedGenerationNonBalancingMarket, WindTotalGenerationForecast, " \
            "PhotovoltaicTotalGenerationForecast, PlannedCrossBorderElectricityExchange, " \
            "ForecastedUnavailabilityTransmissionAndDistribution, " \
            "GenerationCapacityUnavailabilityThermalUnitsBalancingMarket, " \
            "PredictedGenerationNonCoveredByCapacityMarketObligation, CapacityMarketObligationAllUnits " \
            "FROM five_years_plan " \
            "INNER JOIN date ON date.date_id = five_years_plan.date_id " \
            "WHERE date_value = ?"
    return fetch_data_endpoint_by_date(query, 'five_years_plan',
                                       ['id', 'date', 'hour', 'GridDemandForecast',
                                        'RequiredPowerReserve', 'SurplusCapacityAvailableForTSO',
                                        'GenerationCapacitySurplusForTSO',
                                        'AvailableCapacityBalancingMarketUnits',
                                        'AvailableForTSOCapacityBalancingMarketUnits',
                                        'PredictedGenerationBalancingMarket',
                                        'ForecastedGenerationNonBalancingMarket',
                                        'WindTotalGenerationForecast',
                                        'PhotovoltaicTotalGenerationForecast',
                                        'PlannedCrossBorderElectricityExchange',
                                        'ForecastedUnavailabilityTransmissionAndDistribution',
                                        'GenerationCapacityUnavailabilityThermalUnitsBalancingMarket',
                                        'PredictedGenerationNonCoveredByCapacityMarketObligation',
                                        'CapacityMarketObligationAllUnits'], date)


if __name__ == '__main__':
    app.run(debug=True)
