# EnergyGrid-Data-Fetcher
# Energy Data Fetcher

This Python project provides a set of data fetchers for retrieving electricity-related data from different sources. It includes modules for fetching data from Polskie Sieci Energetyczne (PSE) and the Polish Power Exchange (TGE). The data is fetched for specific date ranges and returned as pandas DataFrames.

## Table of Contents

- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Data Fetchers](#data-fetchers)
  - [PSE5YearsPlanDataFetcher](#pse5yearsplandatafetcher)
  - [PSEBalancingMarketFetcher](#psebalancingmarketfetcher)
  - [PSECurrentDailyCoordinationPlanFetcher](#psecurrentdailycoordinationplanfetcher)
  - [DayAheadDataFetcher](#dayaheaddatafetcher)
  - [IntraDayMarketFetcher](#intradaymarketfetcher)
- [DataFetcherFactory](#datafetcherfactory)
- [Class ServicesEnergy](#class-servicesenergy)
- [Examples](#examples)
- [Database](#database)
  - [Setup Database](#setup-database)
  - [Inserting Data from External Services](#inserting-data-from-external-services)
- [API Documentation](#api-documentation)
  - [Fetch all data](#fetch-all-data)
  - [Fetch data by a specific date](#fetch-data-by-a-specific-date)

## Requirements

- Python 3.9 or higher
- Required Python packages are listed in the `Pipfile` file.

## Project Structure

The project is organized into several modules:

- **fetcher.py**: The main module for data fetching. It contains the implementation of data fetchers and a factory for creating them.
- **setup_sqlite.py** This script is responsible for setting up the SQLite database for the project.
- **save.py** This script is designed to populate the SQLite database with data retrieved from external services.
- **Pipfile**: Specifies project dependencies.
- **README.md**: Project documentation.

## Usage
1. Clone the GitHub repository:<br>
```bash
git clone https://github.com/Kris1986-pl/EnergyGrid-Data-Fetcher.git
```
2. Navigate to the project directory:
```bash
cd EnergyGrid-Data-Fetcher
```
3. Install the project dependencies using pipenv. Make sure to set the environment variable PIPENV_VENV_IN_PROJECT to 1 to create a virtual environment inside the project directory:
```bash
pipenv install
```
4. Activate the virtual environment:
```bash
pipenv shell
```

## Data Fetchers

## PSE5YearsPlanDataFetcher
This data fetcher retrieves data from Polskie Sieci Energetyczne (PSE) for the Coordinated 5-years Plan.
* **fetch_data():** Fetches data and returns a pandas DataFrame.
## PSEBalancingMarketFetcher
This data fetcher retrieves data from PSE for Balancing Market Operation - Energy & Prices on Balancing Market.
* **fetch_data():** Fetches data and returns a pandas DataFrame.
## PSECurrentDailyCoordinationPlanFetcher
This data fetcher retrieves data from PSE for the Current Daily Coordination Plan.
* **fetch_data():** Fetches data and returns a pandas DataFrame.
## DayAheadDataFetcher
This data fetcher retrieves data from the Polish Power Exchange (TGE) for the Day-Ahead Market.
* **fetch_data():** Fetches electricity price data and returns it as a DataFrame.
## IntraDayMarketFetcher
This data fetcher retrieves data from the Polish Power Exchange (TGE) for the Intra Day Market.
* **fetch_data():** Fetches electricity price data and returns it as a DataFrame.
## DataFetcherFactory
The DataFetcherFactory class is a factory for creating data fetchers for different sources and dates.
* **create_data_fetcher(source: str, factory_date: datetime):** Creates a data fetcher for the specified source and date.
## Class ServicesEnergy
```python
class ServicesEnergy:
    DAY_AHEAD = 0
    INTRA_DAY = 1
    PSE_5_YEARS_PLAN = 2
    PSE_BALANCING_MARKET = 3
    PSE_CURRENT_DAILY_COORDINATION_PLAN = 4
```
ServicesEnergy is a class that defines constants representing parameters for fetching data from various energy-related services. Each constant corresponds to a specific service, providing a convenient and readable way to reference these services when retrieving data. The class serves as a central point for managing and organizing the different types of energy services available in the application.
## Examples

```python
from datetime import datetime
from fetcher import DataFetcherFactory

# Example usage:
date = datetime(2023, 12, 12)
data_fetcher_factory = DataFetcherFactory()

try:
    # Create a PSE data fetcher
    pse_5_fetcher = data_fetcher_factory.create_data_fetcher(ServicesEnergy.PSE_5_YEARS_PLAN, date)
    print(pse_5_fetcher.fetch_data())
except ValueError as ve:
    # Handle other ValueErrors
    print(f"Error: {ve}")

# ... Repeat the above try-except blocks for other data fetchers

```
## Database

### Setup Database
This project utilizes the SQLite database management system (DBMS). To create the necessary tables, execute the following command in the terminal:

```bash
python setup_sqlite.py
```
### Inserting Data from External Services
If you want to populate the database with data from external services, run the following command in the terminal:
```bash
python save.py
```

# API Documentation

## Overview

This API provides access to energy-related data, including day-ahead prices, intra-day statistics, current daily plans, balancing market information, and five-years plans. The data is organized by date and hour.

## Endpoints
### Fetch all data
#### Fetch Day-Ahead Data
```plaintext
GET /days-ahead
```
#### Fetch Intra Day Market
```plaintext
GET /intra-days
```
#### PSE 5-years Plan
```plaintext
GET /five-years-plans
```
#### PSE Balancing Market
```plaintext
GET /balancing-markets
```
#### PSE Current Daily Coordination Plan
```plaintext
GET /current-daily-plans
```

### Fetch data by a specific date
#### Fetch Day-Ahead Data
```plaintext
GET /days-ahead/:date
:date - Valid format: YYYY-MM-DD
```
#### Fetch Intra Day Market
```plaintext
GET /intra-days/:date
:date - Valid format: YYYY-MM-DD
```
#### PSE 5-years Plan
```plaintext
GET /five-years-plans/:date
:date - Valid format: YYYY-MM-DD
```
#### PSE Balancing Market
```plaintext
GET /balancing-markets/:date
:date - Valid format: YYYY-MM-DD
```
#### PSE Current Daily Coordination Plan
```plaintext
GET /current-daily-plans/:date
:date - Valid format: YYYY-MM-DD
```
