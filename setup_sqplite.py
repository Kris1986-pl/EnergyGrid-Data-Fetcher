from database import Database
import sqlite3


def setup_command():
    try:
        db = Database("energy.db")
        db.insert_data('CREATE TABLE date '
                        '(date_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_value DATE UNIQUE)')
        db.insert_data('CREATE TABLE day_ahead '
                        '(day_ahead_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_id INTEGER REFERENCES date(data_id),'
                        'hour_of_day INTEGER,'
                        'price DECIMAL(10, 2),'
                        'UNIQUE (date_id, hour_of_day))')
        db.insert_data('CREATE TABLE intra_day '
                        '(intra_day_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_id INTEGER REFERENCES date(data_id),'
                        'hour_of_day INTEGER,'
                        'intraday_avg_price DECIMAL(10, 2),'
                        'intraday_min_price DECIMAL(10, 2),'
                        'intraday_max_price DECIMAL(10, 2),'
                        'UNIQUE (date_id, hour_of_day))')
        db.insert_data('CREATE TABLE current_daily_plan '
                        '(current_daily_plan_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_id INTEGER REFERENCES date(data_id),'
                        'hour_of_day INTEGER,'
                        'NationalPowerDemand DECIMAL(10, 2),'  # Krajowe zapotrzebowanie na moc
                        'TotalProductionCapacity_KSE DECIMAL(10, 2),'  # Suma zdolności wytwórczych jednostek wytwórczych w KSE
                        'TotalProductionCapacity_JGWa DECIMAL(10, 2),'  # Suma zdolności wytwórczych JGWa
                        'TotalProductionCapacity_JGFWa DECIMAL(10, 2),'  # Suma zdolności wytwórczych JGFWa
                        'TotalProductionCapacity_JGMa DECIMAL(10, 2),'  # Suma zdolności wytwórczych JGMa
                        'TotalProductionCapacity_JGPVa DECIMAL(10, 2),'  # Suma zdolności wytwórczych JGPVa
                        'TotalGeneration_ActiveJG  DECIMAL(10, 2),'  # Sumaryczna generacja JG aktywnych: JGWa, JGFWa, JGMa i JGPVa 
                        'TotalGeneration_JGWa DECIMAL(10, 2),'  # Sumaryczna generacja JGWa
                        'TotalGeneration_JGFWa DECIMAL(10, 2),'  # Sumaryczna generacja JGFWa
                        'TotalGeneration_JGMa DECIMAL(10, 2),'  # Sumaryczna generacja JGMa                  
                        'TotalGeneration_JGPVa DECIMAL(10, 2),'  # Sumaryczna generacja JGPVa     
                        'TotalGeneration_NonParticipatingUnits DECIMAL(10, 2),'  # Sumaryczna generacja jednostek wytwórczych nieuczestniczących aktywnie w Rynku Bilansującym      
                        'WindPowerGeneration DECIMAL(10, 2),'  # Generacja źródeł wiatrowych                 
                        'PVPowerGeneration DECIMAL(10, 2),'  # Generacja źródeł fotowoltaicznych               
                        'TotalChargingCapacity_JGMa DECIMAL(10, 2),'  # Sumaryczna moc ładowania JGMa                 
                        'NationalParallelExchangeBalance DECIMAL(10, 2),'  # Krajowe saldo wymiany międzysystemowej równoległej            
                        'NationalNonParallelExchangeBalance DECIMAL(10, 2),'  # Krajowe saldo wymiany międzysystemowej nierównoległej                   
                        'ExcessCapacityAboveDemand DECIMAL(10, 2),'  # Rezerwa mocy ponad zapotrzebowanie             
                        'ExcessCapacityBelowDemand DECIMAL(10, 2),'  # Rezerwa mocy poniżej zapotrzebowania                          
                        'TotalCapacityFromUtilizedLoadReductionOffers_JGOa DECIMAL(10, 2),'  # Suma mocy z wykorzystanych Ofert Redukcji Obciążenia JGOa
                        'UNIQUE (date_id, hour_of_day))')
        db.insert_data('CREATE TABLE balancing_market '
                        '(balancing_market_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_id INTEGER REFERENCES date(data_id),'
                        'hour_of_day INTEGER,'
                        'CRO DECIMAL(10, 2),'
                        'CROs DECIMAL(10, 2),'
                        'CROz DECIMAL(10, 2),'
                        'AggregatedMarketParticipantsContractingStatus DECIMAL(10, 2),'  # Stan zakontraktowania
                        'Imbalance DECIMAL(10, 2),'  # Niezbilansowanie
                        'UNIQUE (date_id, hour_of_day))')
        db.insert_data('CREATE TABLE five_years_plan '
                        '(five_years_plan_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'date_id INTEGER REFERENCES date(data_id),'
                        'hour_of_day INTEGER,'
                        'GridDemandForecast DECIMAL(10, 2),'  # Prognozowane zapotrzebowanie sieci
                        'RequiredPowerReserve DECIMAL(10, 2),'  # Wymagana rezerwa mocy OSP
                        'SurplusCapacityAvailableForTSO DECIMAL(10, 2),'  # Nadwyżka mocy dostępna dla OSP (7) + (9) - [(3) - (12)] - (13)
                        'GenerationCapacitySurplusForTSO DECIMAL(10, 2),'  # Nadwyżka mocy dostępna dla OSP ponad wymaganą rezerwę moc (5) - (4)
                        'AvailableCapacityBalancingMarketUnits DECIMAL(10, 2),'  # Moc dyspozycyjna JW i magazynów energii świadczących usługi bilansujące w ramach RB
                        'AvailableForTSOCapacityBalancingMarketUnits DECIMAL(10, 2),'  # Moc dyspozycyjna JW i magazynów energii świadczących usługi bilansujące w ramach RB dostępna dla OSP
                        'PredictedGenerationBalancingMarket DECIMAL(10, 2),'  # Przewidywana generacja JW i magazynów energii świadczących usługi bilansujące w ramach RB (3) - (9)
                        'ForecastedGenerationNonBalancingMarket DECIMAL(10, 2),'  # Prognozowana generacja JW i magazynów energii nie świadczących usług bilansujących w ramach RB
                        'WindTotalGenerationForecast DECIMAL(10, 2),'  # Prognozowana sumaryczna generacja źródeł wiatrowych
                        'PhotovoltaicTotalGenerationForecast DECIMAL(10, 2),'  # Prognozowana sumaryczna generacja źródeł fotowoltaicznych
                        'PlannedCrossBorderElectricityExchange DECIMAL(10, 2),'  # Planowane saldo wymiany międzysystemowej
                        'ForecastedUnavailabilityTransmissionAndDistribution DECIMAL(10, 2),'  # Prognozowana wielkość niedyspozycyjności wynikająca z ograniczeń sieciowych występujących w sieci przesyłowej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej
                        'GenerationCapacityUnavailabilityThermalUnitsBalancingMarket DECIMAL(10, 2),'  # Prognozowana wielkość niedyspozycyjności wynikających z warunków eksploatacyjnych JW świadczących usługi bilansujące w ramach RB
                        'PredictedGenerationNonCoveredByCapacityMarketObligation DECIMAL(10, 2),'  # Przewidywana generacja zasobów wytwórczych nieobjętych obowiązkami mocowymi
                        'CapacityMarketObligationAllUnits DECIMAL(10, 2),'  # Obowiązki mocowe wszystkich jednostek rynku mocy
                        'UNIQUE (date_id, hour_of_day))')
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        print("Table created successfully!")


if __name__ == "__main__":
    setup_command()
