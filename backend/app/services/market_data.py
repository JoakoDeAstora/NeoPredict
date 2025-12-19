import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from app.config import CLUSTERS_CONFIG

# Configuración de logs para ver errores en la nube
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MarketDataService")

class MarketDataService:
    def __init__(self):
        """
        Servicio encargado de extraer datos NUMÉRICOS (Variación, Precio, Volumen)
        de fuentes financieras como Yahoo Finance.
        """
        pass

    async def get_annual_data(self, ticker_key: str):
        """
        Obtiene el movimiento financiero del último año para la empresa solicitada.
        
        Args:
            ticker_key (str): La clave interna (ej: "SQM-B", "CHILE").
            
        Returns:
            dict: Diccionario con la variación anual calculada y precios.
                  Retorna None si falla.
        """
        try:
            # 1. Obtener configuración del Ticker (ej: SQM-B -> SQM-B.SN)
            config = CLUSTERS_CONFIG.get(ticker_key)
            if not config or "yahoo_ticker" not in config:
                logger.error(f"❌ Configuración no encontrada o incompleta para {ticker_key}")
                return None

            yahoo_symbol = config["yahoo_ticker"]
            logger.info(f"📈 Descargando datos financieros para {ticker_key} ({yahoo_symbol})...")

            # 2. Conexión a Yahoo Finance
            # Usamos 'period="1y"' para obtener todo el movimiento anual necesario para tu red neuronal
            stock = yf.Ticker(yahoo_symbol)
            hist = stock.history(period="1y")

            if hist.empty:
                logger.warning(f"⚠️ No se encontraron datos históricos para {yahoo_symbol}")
                return None

            # 3. Calcular la Variación Anual (Input clave para tu IA)
            # Fórmula: (Precio Actual - Precio Hace 1 Año) / Precio Hace 1 Año
            price_start = hist['Close'].iloc[0] # Precio hace un año
            price_end = hist['Close'].iloc[-1]  # Precio de hoy
            
            variation_percent = ((price_end - price_start) / price_start)
            
            # Datos adicionales (Volumen promedio, volatilidad) pueden agregarse aquí
            volume_avg = hist['Volume'].mean()

            logger.info(f"✅ Datos obtenidos {ticker_key}: Variación {variation_percent:.2%}")

            # 4. Estructurar la respuesta
            return {
                "ticker": ticker_key,
                "date": datetime.now().isoformat(),
                "price_start": round(price_start, 2),
                "price_end": round(price_end, 2),
                "annual_variation": float(variation_percent), # Este es el dato que irá a tu Red Neuronal
                "avg_volume": float(volume_avg),
                "currency": "CLP" # Asumimos pesos chilenos por el .SN
            }

        except Exception as e:
            logger.error(f"❌ Error crítico obteniendo datos para {ticker_key}: {str(e)}")
            return None

    def get_real_time_price(self, ticker_key: str):
        """
        Método auxiliar por si necesitas el precio instantáneo para la App Móvil.
        """
        try:
            config = CLUSTERS_CONFIG.get(ticker_key)
            if not config: return None
            
            stock = yf.Ticker(config["yahoo_ticker"])
            # 'fast_info' es más rápido que 'history' para datos actuales
            price = stock.fast_info.last_price
            return price
        except:
            return 0.0