from database import Database


def setup_command():
    db = Database("energy.db")
    db.create_table('CREATE TABLE date '
                    '(date_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'date_value DATE)')
    db.create_table('CREATE TABLE day_ahead '
                    '(day_ahead_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'date_id INTEGER REFERENCES date(data_id),'
                    'price DECIMAL(10, 2))')
    db.create_table('CREATE TABLE intra_day '
                    '(intra_day_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'date_id INTEGER REFERENCES date(data_id),'
                    'hour_of_day INTEGER,'
                    'intraday_avg_price DECIMAL(10, 2),'
                    'intraday_min_price DECIMAL(10, 2),'
                    'intraday_max_price DECIMAL(10, 2))')
    db.create_table('CREATE TABLE current_daily_plan '
                    '(intra_day_id INTEGER PRIMARY KEY AUTOINCREMENT, '
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
                    'TotalCapacityFromUtilizedLoadReductionOffers_JGOa DECIMAL(10, 2))')  # Suma mocy z wykorzystanych Ofert Redukcji Obciążenia JGOa
    db.create_table('CREATE TABLE balancing_market '
                    '(intra_day_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'date_id INTEGER REFERENCES date(data_id),'
                    'hour_of_day INTEGER,'
                    'CRO DECIMAL(10, 2),'
                    'CROs DECIMAL(10, 2),'
                    'CROz DECIMAL(10, 2),'
                    'AggregatedMarketParticipantsContractingStatus DECIMAL(10, 2),'  # Stan zakontraktowania
                    'Imbalance DECIMAL(10, 2))')  # Niezbilansowanie


if __name__ == "__main__":
    setup_command()
