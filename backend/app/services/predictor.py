import torch
import numpy as np
from app.services.market_data import MarketDataService
from app.services.sentiment import SentimentService
from app.models.hybrid_model import HybridPredictor
from app.services.scraper import CmfScraperService

class PredictionService:
    def __init__(self):
        self.market_data = MarketDataService()
        self.sentiment = SentimentService()
        self.scraper = CmfScraperService()
        
        # Load Model
        self.model = HybridPredictor()
        # In a real scenario, we would load weights here:
        # self.model.load_state_dict(torch.load("path/to/weights.pth"))
        self.model.eval()

    async def predict_year(self, ticker: str, year: int):
        """
        Orchestrates the prediction pipeline.
        1. Get numeric history up to (year-1)
        2. Get text sentiment for year-1 (or current available)
        3. Predict
        """
        # 1. Numeric Data
        history = await self.market_data.get_annual_data(ticker)
        # Filter strictly before target year for causality
        past_data = [d for d in history if d['year'] < year]
        
        if len(past_data) < 5:
            # Need at least some history for LSTM
            return {"error": "Insufficient historical data"}
            
        # Prepare numeric tensor (last 5 years for simple lag)
        recent_years = past_data[-5:]
        numeric_features = [[d['close'], d['volume'], d['volatility'], d['high'], d['low']] for d in recent_years]
        numeric_tensor = torch.tensor([numeric_features], dtype=torch.float32) # Batch size 1
        
        # 2. Sentiment Data
        # Try to find memory for year-1
        prev_year = year - 1
        # For demo purposes, since we can't scrape, we might simulate sentiment
        # or use a placeholder text if scraping fails
        sentiment_text = f"Memoria anual {ticker} {prev_year}. El año presentó desafíos en el mercado del litio y volatilidad cambiaria..."
        
        # If we had the scraper working:
        # pdf_path = self.scraper.search_annual_report(ticker, prev_year)
        # if pdf_path: text = self.scraper.extract_text(pdf_path) ...
        
        text_embedding = self.sentiment.get_embedding(sentiment_text)
        
        # 3. Predict
        with torch.no_grad():
            probs = self.model(numeric_tensor, text_embedding)
        
        # Interpretation
        classes = ["Bearish", "Neutral", "Bullish"]
        prediction_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0][prediction_idx].item()
        
        result = {
            "target_year": year,
            "prediction": classes[prediction_idx],
            "confidence": confidence,
            "probabilities": {
                "bearish": probs[0][0].item(),
                "neutral": probs[0][1].item(),
                "bullish": probs[0][2].item()
            },
            "sentiment_summary": self.sentiment.analyze_text(sentiment_text, ticker=ticker) 
        }
        
        # 4. Post-Processing (Cluster Specific Logic)
        from app.config import CLUSTERS_CONFIG
        config = CLUSTERS_CONFIG.get(ticker)
        if config and ticker == "COPEC":
            # Inhibition Neuron Logic: If Forestry/Celulosa sentiment is very negative, reduce confidence
            # This simulates the "inhibition" of that driver in the final output
            if "Celulosa" in sentiment_text and result['sentiment_summary'] < -0.3:
                 result['confidence'] *= 0.8 # Reduce confidence/weight
                 result['note'] = "Forestry driver inhibited due to negative outlook."
        
        return result
