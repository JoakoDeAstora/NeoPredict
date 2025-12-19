from app.services.market_data import MarketDataService
from app.services import data_service
from app.config import CLUSTERS_CONFIG
# Ya no necesitamos 'apscheduler' ni 'asyncio' explícito aquí si usamos FastAPI correctamente

class UpdaterService:
    def __init__(self):
        self.market_service = MarketDataService()
        # ELIMINADO: self.scheduler = BackgroundScheduler() -> Ya no es necesario

    # ELIMINADO: def start(self): ... 
    # Ya no arrancamos un reloj interno. La nube nos "despierta" cuando es hora.

    async def run_update_cycle(self):
        """
        Esta función ahora es 'async' para ser llamada directamente 
        desde el endpoint de FastAPI en main.py sin bloquear el servidor.
        """
        print(" [UPDATER] Starting update cycle triggered by Cloud Scheduler...")
        
        # Llamamos directamente a la lógica interna
        await self._update_all_tickers()

    async def _update_all_tickers(self):
        from app.services.scraper import CmfScraperService
        scraper = CmfScraperService()
        
        for ticker, config in CLUSTERS_CONFIG.items():
            try:
                print(f" [UPDATER] Updating {ticker}...")
                
                # 1. Fetch Market Data (Simulado o Real)
                # data = await self.market_service.get_annual_data(ticker)
                # if data: data_service.save_market_data(ticker, data)

                # 2. Run Robot Recolector (Web Scraping)
                if hasattr(config, 'investor_url') and config.investor_url:
                    # Nota: Si scraper.visit_investor_site NO es async, lo ejecutamos directo.
                    # Si fuera async, usaríamos 'await'. Asumo que es síncrono por tu código anterior.
                    content = scraper.visit_investor_site(ticker, config.investor_url)
                    
                    if content:
                        clean_content = scraper.clean_text(content)
                        # Guardar datos no estructurados
                        data_service.save_unstructured_data(ticker, clean_content, config.investor_url)
                        
                        # Aquí iría la predicción (Fase 3)
                        
                print(f" [UPDATER] Success cycle for {ticker}")

            except Exception as e:
                print(f" [UPDATER] Error updating {ticker}: {str(e)}")