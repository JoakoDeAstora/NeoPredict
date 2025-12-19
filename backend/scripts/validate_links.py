import requests
import sys
import os

# Asegurar que encuentra la carpeta app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import CLUSTERS_CONFIG

def validate_sources():
    print("🔍 Iniciando validación de fuentes de datos...")
    
    headers = {'User-Agent': 'Mozilla/5.0'} # Para no parecer un bot malicioso
    
    for ticker, data in CLUSTERS_CONFIG.items():
        url = data['investor_url']
        print(f"Testing {ticker} ({data['sector']})...", end=" ")
        
        try:
            # Hacemos una petición HEAD (o GET) para ver si la web responde 200 OK
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ OK")
                
                # Validación extra: ¿Están las palabras clave?
                missing_keywords = [k for k in data['keywords'] if k not in response.text]
                if missing_keywords:
                    print(f"   ⚠️  Advertencia: No encontré las palabras clave {missing_keywords} en la portada.")
            else:
                print(f"❌ ERROR ({response.status_code})")
                print(f"   Revisar URL: {url}")
                
        except Exception as e:
            print(f"❌ FALLÓ: {str(e)}")

if __name__ == "__main__":
    validate_sources()