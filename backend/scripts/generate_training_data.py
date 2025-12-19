import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- Configuration ---
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'neopredict.db')
START_DATE = '2020-01-01'
END_DATE = '2025-12-18'

def create_schema(conn):
    cursor = conn.cursor()
    
    # 1. Companies
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        sector TEXT,
        cluster TEXT
    )
    ''')
    
    # 2. Macro Indicators (Drivers)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS macro_indicators (
        date TEXT PRIMARY KEY,
        tpm REAL,           -- Tasa Politica Monetaria
        uf_value REAL,      -- Unidad de Fomento
        usd_clp REAL,       -- Dolar
        lithium_price REAL, -- Carbonato de Litio
        brent_oil REAL,     -- Petroleo
        pulp_price REAL,    -- Celulosa
        jet_fuel REAL       -- Kerosene Avion
    )
    ''')
    
    # 3. Stock Market Data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_market_data (
        date TEXT,
        ticker TEXT,
        close_price REAL,
        volume INTEGER,
        volatility_index REAL,
        PRIMARY KEY (date, ticker),
        FOREIGN KEY (ticker) REFERENCES companies(ticker)
    )
    ''')
    
    # 4. Sentiment Logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sentiment_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        ticker TEXT,
        source TEXT,
        keyword_detected TEXT,
        sentiment_score REAL, -- -1.0 to 1.0
        context TEXT,
        FOREIGN KEY (ticker) REFERENCES companies(ticker)
    )
    ''')
    conn.commit()

def generate_macro_data(dates):
    # Generating realistic-looking random walks for drivers
    n = len(dates)
    
    # Lithium: Boom in 2021-2022, correction in 2023-2024
    lithium_trend = np.linspace(10000, 80000, n) # Base trend
    # Add boom shape manually
    boom_factor = np.exp(-((np.arange(n) - n*0.6)**2) / (n*0.1)**2) * 50000 
    lithium = lithium_trend + boom_factor + np.random.normal(0, 2000, n)
    
    # Oil: Volatile but mean reverting
    oil = 70 + np.cumsum(np.random.normal(0, 1.5, n))
    oil = np.clip(oil, 40, 120)
    
    # Jet Fuel is correlated with Oil
    jet_fuel = oil * 1.2 + np.random.normal(0, 2, n)
    
    # USD/CLP: Rising trend
    usd_clp = np.linspace(750, 950, n) + np.cumsum(np.random.normal(0, 2, n))
    
    # Pulp: Cyclical
    pulp = 800 + 200 * np.sin(np.arange(n) / 100) + np.random.normal(0, 10, n)
    
    # TPM: Low in 2020, high in 2023, falling in 2025
    tpm = np.zeros(n)
    tpm[:int(n*0.4)] = 0.5 # Low
    tpm[int(n*0.4):int(n*0.8)] = np.linspace(0.5, 11.25, int(n*0.8)-int(n*0.4)) # Hiking
    tpm[int(n*0.8):] = np.linspace(11.25, 4.5, n-int(n*0.8)) # Cuts
    
    # UF: Constant inflation acc
    uf = np.linspace(28000, 38000, n)

    df_macro = pd.DataFrame({
        'date': dates,
        'tpm': tpm,
        'uf_value': uf,
        'usd_clp': usd_clp,
        'lithium_price': lithium,
        'brent_oil': oil,
        'pulp_price': pulp,
        'jet_fuel': jet_fuel
    })
    return df_macro

def generate_company_data(conn, macro_df):
    companies = [
        ('SQM-B', 'Sociedad Química y Minera', 'Minería', 'Commodities'),
        ('CHILE', 'Banco de Chile', 'Financiero', 'Domestic'),
        ('CENCOSUD', 'Cencosud S.A.', 'Retail', 'Domestic'),
        ('COPEC', 'Empresas Copec', 'Energía', 'Commodities/Domestic'),
        ('ENELAM', 'Enel Américas', 'Utilities', 'Domestic'),
        ('LTM', 'Latam Airlines', 'Transporte', 'Idiosyncratic'),
    ]
    
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO companies VALUES (?,?,?,?)', companies)
    
    stock_records = []
    sentiment_records = []
    
    dates = pd.to_datetime(macro_df['date'])
    
    for ticker, name, sec, clust in companies:
        base_price = 100.0
        prices = []
        
        for i, row in macro_df.iterrows():
            date_str = row['date']
            current_date = dates[i]
            
            # --- STOCK PRICE LOGIC (Correlations) ---
            variation = np.random.normal(0, 0.015) # Daily random noise
            
            # SQM Logic: Lithium Driver
            if ticker == 'SQM-B':
                # Lithium Impact (Lagged slightly/smoothed)
                lit_pct = (row['lithium_price'] / 40000.0) - 1.0 # 0 baseline
                variation += lit_pct * 0.002 # Sensitivity
                
            # LTM Logic: Jet Fuel & Pandemic
            elif ticker == 'LTM':
                fuel_drag = (row['jet_fuel'] / 80.0) - 1.0
                variation -= fuel_drag * 0.003
                
                # Chapter 11 Exit Jump (Nov 2022)
                if current_date == pd.Timestamp('2022-11-03'):
                    variation += 0.15 # 15% jump
                    
            # COPEC Logic: Mix Pulp + Oil
            elif ticker == 'COPEC':
                pulp_eff = (row['pulp_price'] / 900.0) - 1.0
                oil_eff = (row['brent_oil'] / 70.0) - 1.0
                variation += (pulp_eff * 0.4 + oil_eff * 0.2) * 0.002
                
            # CHILE Logic: TPM/Rates benefit banks (sort of)
            elif ticker == 'CHILE':
                rate_eff = (row['tpm'] / 5.0) - 1.0
                variation += rate_eff * 0.001
            
            # Update Price
            base_price = base_price * (1 + variation)
            prices.append(max(base_price, 1.0))
            
            # --- SENTIMENT LOGS LOGIC ---
            # Inject events randomly but with correct bias defined in text
            if np.random.random() < 0.02: # 2% chance of news per day
                
                if ticker == 'SQM-B':
                    if np.random.random() < 0.3:
                        keyword = "Royalty"
                        score = -0.8
                        txt = "Gobierno discute nuevo Royalty minero"
                    else:
                        keyword = "China"
                        score = 0.7
                        txt = "China aumenta demanda de VEs"
                        
                elif ticker == 'LTM':
                     if current_date < pd.Timestamp('2022-11-01'):
                         keyword = "Chapter 11"
                         score = -0.4
                         txt = "Proceso de reestructuración continúa"
                     else:
                         keyword = "Exit"
                         score = 0.8
                         txt = "Salida exitosa del Capítulo 11"
                         
                elif ticker == 'ENELAM':
                    if row['usd_clp'] > 900: # High dollar bad for debt
                         keyword = "Tipo de Cambio"
                         score = -0.6
                         txt = "Impacto por alza del dólar en deuda"
                    else:
                         keyword = "Hidrología"
                         score = 0.5
                         txt = "Mejora en niveles de embalses"
                
                else:
                    keyword = "Resultados"
                    score = np.random.uniform(-0.5, 0.5)
                    txt = "Reporte trimestral publicado"
                
                sentiment_records.append((date_str, ticker, "News", keyword, score, txt))
        
        # Add to records
        for i, p in enumerate(prices):
            vol = int(np.random.normal(1000000, 200000))
            volatility = np.std(prices[max(0, i-30):i+1]) # Rolling std
            stock_records.append((macro_df.iloc[i]['date'], ticker, round(p, 2), vol, round(volatility, 3)))

    cursor.executemany('INSERT INTO stock_market_data VALUES (?,?,?,?,?)', stock_records)
    cursor.executemany('INSERT INTO sentiment_logs (date, ticker, source, keyword_detected, sentiment_score, context) VALUES (?,?,?,?,?,?)', sentiment_records)
    conn.commit()

def main():
    print(f"Generando DB en: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    create_schema(conn)
    
    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    df_macro = generate_macro_data(date_range)
    
    # Save macro
    df_macro.to_sql('macro_indicators', conn, if_exists='replace', index=False)
    
    generate_company_data(conn, df_macro)
    
    conn.close()
    print("Base de datos generada exitosamente. Lista para entrenar.")

if __name__ == "__main__":
    main()
