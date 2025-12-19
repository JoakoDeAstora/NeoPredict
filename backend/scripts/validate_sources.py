import sys
import os
import requests
import yfinance as yf

# Truco para importar módulos de la carpeta 'app' desde un script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import CLUSTERS_CONFIG

def test_integration():
    print("🚀 INICIANDO VALIDACIÓN FASE 4 (GCP PRE-DEPLOY)\n")
    print(f"{'EMPRESA':<15} | {'YAHOO FINANCE':<15} | {'WEB INVERSIONISTAS':<15}")
    print("-" * 55)

    headers = {'User-Agent': 'Mozilla/5.0'}

    for ticker, data in CLUSTERS_CONFIG.items():
        yahoo_status = "⏳ ..."
        web_status = "⏳ ..."
        
        # 1. PRUEBA YAHOO FINANCE (Números)
        try:
            stock = yf.Ticker(data['yahoo_ticker'])
            hist = stock.history(period="5d") # Pedimos 5 días
            if not hist.empty:
                yahoo_status = "✅ OK"
            else:
                yahoo_status = "❌ VACÍO"
        except Exception as e:
            yahoo_status = "❌ ERROR"

        # 2. PRUEBA SITIO WEB (Texto)
        try:
            resp = requests.head(data['investor_url'], headers=headers, timeout=10)
            # Algunas webs bloquean HEAD, si falla probamos GET
            if resp.status_code != 200:
                resp = requests.get(data['investor_url'], headers=headers, timeout=10)
            
            if resp.status_code == 200:
                web_status = "✅ OK"
            else:
                web_status = f"⚠️ {resp.status_code}"
        except:
            web_status = "❌ TIMEOUT"

        print(f"{ticker:<15} | {yahoo_status:<15} | {web_status:<15}")

    print("\n🏁 Validación terminada.")
    print("Si ves ✅ en ambas columnas, estás listo para la Fase 5.")

if __name__ == "__main__":
    test_integration()