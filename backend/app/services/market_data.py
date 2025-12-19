import yfinance as yf
import pandas as pd
from datetime import datetime

class MarketDataService:
    def __init__(self):
        # IPSA Tickers mapping (Yahoo Finance)
        self.tickers = {
            "SQM_B": "SQM-B.SN",
            "CHILE": "CHILE.SN",
            "CENCOSUD": "CENCOSUD.SN",
            "COPEC": "COPEC.SN",
            "ENELAM": "ENELAM.SN",
            "LTM": "LTM.SN"
        }

    async def get_annual_data(self, ticker_key: str):
        """
        Fetches daily data and resamples it to annual metrics.
        """
        if ticker_key not in self.tickers:
            raise ValueError(f"Ticker {ticker_key} not found in supported list.")
        
        symbol = self.tickers[ticker_key]
        ticker = yf.Ticker(symbol)
        
        # Download max history
        df = ticker.history(period="max")
        
        if df.empty:
            return []

        # Annual Resampling
        # We want: Close price at year end, Annual Volatility, Total Volume, High, Low
        annual_df = df.resample('Y').agg({
            'Close': 'last',
            'Volume': 'sum',
            'High': 'max',
            'Low': 'min'
        })
        
        # Calculate Annual Volatility (Standard deviation of daily returns * sqrt(252))
        daily_returns = df['Close'].pct_change()
        annual_volatility = daily_returns.resample('Y').std() * (252**0.5)
        
        annual_df['Volatility'] = annual_volatility
        
        # Reset index to make Date a column and formatted keys
        data = []
        for index, row in annual_df.iterrows():
            data.append({
                "year": index.year,
                "close": row['Close'],
                "volatility": row['Volatility'] if not pd.isna(row['Volatility']) else 0.0,
                "volume": row['Volume'],
                "high": row['High'],
                "low": row['Low']
            })
            
        return data

    async def get_latest_price(self, ticker_key: str):
        if ticker_key not in self.tickers:
            raise ValueError(f"Ticker {ticker_key} not found")
            
        symbol = self.tickers[ticker_key]
        ticker = yf.Ticker(symbol)
        # Get fast info
        return ticker.fast_info.last_price
