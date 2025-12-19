import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'backend', 'data', 'neopredict.db')

def get_monthly_data(ticker: str):
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Get Stock Prices (Daily -> Monthly Avg)
    query_stock = f"""
    SELECT date, close_price 
    FROM stock_market_data 
    WHERE ticker = '{ticker}'
    ORDER BY date ASC
    """
    df_stock = pd.read_sql_query(query_stock, conn)
    df_stock['date'] = pd.to_datetime(df_stock['date'])
    df_stock.set_index('date', inplace=True)

    # --- Data Cleaning / Adjustment Layer ---
    if ticker == "CENCOSUD":
        # Rule: Filter IAS 29 (Hyperinflation Argentina) effect
        # Assuming we have a column 'adjustment_factor' or similar, otherwise mock the adjustment
        # reducing nominal growth hallucinations.
        # df_stock['close_price'] = df_stock['close_price'] * df_stock['ias29_factor']
        pass # Placeholder for actual logic
    
    if ticker == "ENELAM":
        # Rule: Adjust for FX (CLP/USD or local currencies)
        # df_stock['close_price'] = df_stock['close_price'] / df_stock['fx_rate']
        pass
    # ----------------------------------------
    
    # Resample to Monthly End
    monthly_prices = df_stock['close_price'].resample('ME').mean()
    
    # 2. Get Sentiment (Daily -> Monthly Avg)
    query_sent = f"""
    SELECT date, sentiment_score 
    FROM sentiment_logs 
    WHERE ticker = '{ticker}'
    """
    df_sent = pd.read_sql_query(query_sent, conn)
    if not df_sent.empty:
        df_sent['date'] = pd.to_datetime(df_sent['date'])
        df_sent.set_index('date', inplace=True)
        monthly_sent = df_sent['sentiment_score'].resample('ME').mean().fillna(0)
    else:
        monthly_sent = pd.Series(0, index=monthly_prices.index)

    # 3. Merge
    df_final = pd.DataFrame({
        'price': monthly_prices,
        'sentiment': monthly_sent
    }).fillna(0)
    
    # Format for API
    results = []
    for date, row in df_final.iterrows():
        results.append({
            "year": date.year + (date.month - 1) / 12.0, # Decimal year for easier charting (2020.0, 2020.08...)
            "value": round(row['price'], 2),
            "sentimentScore": round(row['sentiment'], 3)
        })
        
    return results

def get_prediction_data(ticker: str):
    # Mocking prediction based on latest db data trends
    # In a real scenario, this would call the LSTM model inference
    # For now, we project the last known value
    
    last_hist = get_monthly_data(ticker)[-1]
    base_val = last_hist['value']
    base_year = last_hist['year']
    
    # Simple linear protection mock
    predictions = []
    for i in range(1, 13): # Next 12 months
        proj_year = base_year + (i/12.0)
        # Random walk projection
        predictions.append({
            "year": proj_year,
            "value": round(base_val * (1 + 0.01 * i), 2), # 1% growth/month mock
            "sentimentScore": 0.2
        })
    return predictions

def save_market_data(ticker: str, data_list: list):
    """
    Saves a list of market data points to the database.
    Upserts (Insert or Replace) to avoid duplicates.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure table exists (create if not - for safety/demo)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_market_data (
        ticker TEXT,
        date TEXT,
        close_price REAL,
        volume REAL,
        volatility REAL,
        high REAL,
        low REAL,
        PRIMARY KEY (ticker, date)
    )
    """)
    
    for item in data_list:
        # Assuming item has 'year' as int (annual) or date string.
        # If 'year', we default to end of year date: YYYY-12-31
        date_str = f"{item['year']}-12-31" if isinstance(item.get('year'), int) else str(item.get('date'))
        
        cursor.execute("""
        INSERT OR REPLACE INTO stock_market_data (ticker, date, close_price, volume, volatility, high, low)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticker, 
            date_str, 
            item.get('close') or item.get('value'), # handle different key names
            item.get('volume', 0), 
            item.get('volatility', 0),
            item.get('high', 0),
            item.get('low', 0)
        ))
        
    conn.commit()
    conn.close()
    conn.commit()
    conn.close()
    print(f"[DB] Saved {len(data_list)} records for {ticker}")

def save_unstructured_data(ticker: str, content: str, source_url: str):
    """
    [Phase 2: Use of DB]
    Saves text content (news, reports) to a separate Unstructured Data table.
    """
    if not content: return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unstructured_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        date TEXT,
        content TEXT,
        source_url TEXT
    )
    """)
    
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
    INSERT INTO unstructured_data (ticker, date, content, source_url)
    VALUES (?, ?, ?, ?)
    """, (ticker, today, content, source_url))
    
    conn.commit()
    conn.close()
    print(f"[DB] Saved unstructured data for {ticker}")

def save_prediction(ticker: str, prediction_data: dict):
    """
    [Phase 3: Saving Predictions]
    Saves the output of the Neural Network.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        ticker TEXT,
        target_year REAL,
        prediction_class TEXT,
        confidence REAL,
        sentiment_summary REAL,
        generated_at TEXT,
        PRIMARY KEY (ticker, target_year)
    )
    """)
    
    cursor.execute("""
    INSERT OR REPLACE INTO predictions (ticker, target_year, prediction_class, confidence, sentiment_summary, generated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        ticker,
        prediction_data['target_year'],
        prediction_data['prediction'],
        prediction_data['confidence'],
        prediction_data['sentiment_summary'],
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    print(f"[DB] Saved prediction for {ticker}")
