
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.market_data import MarketDataService
from app.services import data_service
from app.config import CLUSTERS_CONFIG
import asyncio

class UpdaterService:
    def __init__(self):
        self.market_service = MarketDataService()
        self.scheduler = BackgroundScheduler()

    def start(self):
        """
        Starts the background scheduler.
        Configured to run immediately on startup (for demo) and then every 24 hours.
        """
        # Add job
        self.scheduler.add_job(self.run_update_cycle, 'interval', minutes=1, id='market_update_job') # 1 min for testing
        self.scheduler.start()
        print(" [UPDATER] Background Scheduler Started.")

    def run_update_cycle(self):
        """
        Main logic wrapper to run async code in sync scheduler.
        """
        print(" [UPDATER] Starting update cycle...")
        asyncio.run(self._update_all_tickers())

    async def _update_all_tickers(self):
        from app.services.scraper import CmfScraperService
        scraper = CmfScraperService()
        
        for ticker, config in CLUSTERS_CONFIG.items():
            try:
                print(f" [UPDATER] Updating {ticker}...")
                
                # 1. Fetch Market Data (Annual) - Phase 2 (Historical DB)
                # data = await self.market_service.get_annual_data(ticker) # Commented out to focus on Robot for now or assume mocked
                # if data: data_service.save_market_data(ticker, data)

                # 2. Run Robot Recolector (Web Scraping) - Phase 1
                if hasattr(config, 'investor_url') and config.investor_url:
                    content = scraper.visit_investor_site(ticker, config.investor_url)
                    if content:
                        clean_content = scraper.clean_text(content)
                        # Phase 2: Save Unstructured Data
                        data_service.save_unstructured_data(ticker, clean_content, config.investor_url)
                        
                        # Phase 3: Trigger Neural Network Prediction (Mock Trigger)
                        # In real life: predictor = PredictionService(); result = await predictor.predict_year(ticker, 2025)
                        # data_service.save_prediction(ticker, result)
                        
                print(f" [UPDATER] Success cycle for {ticker}")

            except Exception as e:
                print(f" [UPDATER] Error updating {ticker}: {str(e)}")
