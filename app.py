from flask import Flask, g, jsonify
import sqlite3
import json
from database import Database

app = Flask(__name__)
DATABASE = 'energy.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Add your setup_command function here to create tables

def fetch_data_endpoint(query, endpoint_name, key_names):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Organize the data by date
    data_by_date = {}
    for result in results:
        date_key = result[1]
        record = {key_names[i]: result[i] for i in range(len(key_names))}
        if date_key in data_by_date:
            data_by_date[date_key].append(record)
        else:
            data_by_date[date_key] = [record]

    # Convert the dictionary to a list of dictionaries
    data = [{'date': date, 'records': records} for date, records in data_by_date.items()]

    # Use json.dumps with sort_keys parameter
    ordered_json_data = json.dumps({f'{endpoint_name}_data': data}, sort_keys=False)

    return ordered_json_data


def fetch_data_endpoint_by_date(query, endpoint_name, key_names, date):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, (date,))
    results = cursor.fetchall()

    # Organize the data by date
    data_by_date = {}
    for result in results:
        date_key = result[1]
        record = {key_names[i]: result[i] for i in range(len(key_names))}
        if date_key in data_by_date:
            data_by_date[date_key].append(record)
        else:
            data_by_date[date_key] = [record]

    # Convert the dictionary to a list of dictionaries
    data = [{'date': date, 'records': records} for date, records in data_by_date.items()]

    # Use json.dumps with sort_keys parameter
    ordered_json_data = json.dumps({f'{endpoint_name}_data': data}, sort_keys=False)

    return ordered_json_data


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
