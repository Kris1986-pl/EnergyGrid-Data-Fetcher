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
- [DataFetcherFactory](#datafetcherfactory)
- [Examples](#examples)

## Requirements

- Python 3.9 or higher
- Required Python packages are listed in the `Pipfile` file.

## Project Structure

The project is organized into several modules:

- **main.py**: The main module for data fetching. It contains the implementation of data fetchers and a factory for creating them.
- **Pipfile**: Specifies project dependencies.
- **README.md**: Project documentation.

## Usage
1. Clone the GitHub repository:<br>
```bash
git clone https://github.com/Kris1986-pl/EnergyGrid-Data-Fetcher.git
```
2. Navigate to the project directory:
```bash
cd EnergyGrid-Data-Fetcher-main
```
3. Install the project dependencies using pipenv. Make sure to set the environment variable PIPENV_VENV_IN_PROJECT to 1 to create a virtual environment inside the project directory:
```bash
PIPENV_VENV_IN_PROJECT=1 pipenv install
```
4. Activate the virtual environment:
```bash
pipenv shell
```
5. Create .env file:
```bash
touch .venv 
```
