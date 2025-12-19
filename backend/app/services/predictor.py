import torch
import os
import logging
from google.cloud import storage
from app.models.hybrid_model import FinancialNeuralNet  # Tu modelo de red neuronal
# from app.utils.preprocessing import format_data # Si tienes un formateador específico, impórtalo aquí

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PredictorService")

class PredictionService:
    def __init__(self):
        """
        Inicializa el servicio, descarga los pesos de la nube y prepara el modelo.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Configuración de Google Cloud Storage
        self.bucket_name = "neopredict-weights"  # Nombre de tu Bucket en GCP
        self.remote_weights_name = "model_weights.pth"
        
        # En Cloud Run, solo podemos escribir en /tmp
        self.local_weights_path = "/tmp/model_weights.pth" 

        # 1. Instanciar la arquitectura del modelo
        self.model = FinancialNeuralNet().to(self.device)
        
        # 2. Cargar los pesos (Intenta bajar de la nube, sino usa locales o aleatorios)
        self._load_model_weights()

    def _load_model_weights(self):
        """
        Intenta descargar los pesos desde GCS. Si falla, busca en local.
        """
        try:
            # Opción A: Intentar descargar de Google Cloud Storage
            logger.info("☁️ Conectando a GCS para descargar pesos...")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.remote_weights_name)
            blob.download_to_filename(self.local_weights_path)
            logger.info("✅ Pesos descargados correctamente en /tmp.")
            
            # Cargar en PyTorch
            self.model.load_state_dict(torch.load(self.local_weights_path, map_location=self.device))
            self.model.eval() # IMPORTANTE: Poner en modo evaluación (congela Dropout/Batchnorm)
            logger.info("🧠 Modelo cargado y listo para inferencia.")

        except Exception as e:
            logger.warning(f"⚠️ No se pudo descargar de GCS: {e}")
            logger.info("🔄 Intentando buscar pesos locales de respaldo o iniciando con pesos aleatorios.")
            
            # Opción B: Si tienes un archivo local (para desarrollo offline)
            local_backup = "backend/app/models/weights.pth"
            if os.path.exists(local_backup):
                self.model.load_state_dict(torch.load(local_backup, map_location=self.device))
                self.model.eval()
                logger.info("📂 Modelo local cargado.")
            else:
                logger.warning("⚠️ ¡ADVERTENCIA! El modelo está usando pesos ALEATORIOS (sin entrenar).")

    async def predict_year(self, ticker: str, financial_features: list, sentiment_score: float):
        """
        Realiza la predicción combinando datos numéricos y de texto.
        
        Args:
            ticker (str): Símbolo de la empresa.
            financial_features (list): Lista de floats [ROE, Debt, Assets, etc.]
            sentiment_score (float): Score del análisis de sentimiento (-1 a 1).
        
        Returns:
            dict: Predicción formateada.
        """
        try:
            # 1. Preprocesamiento de datos (Convertir a Tensores)
            # Asumimos que financial_features es una lista de números
            fin_tensor = torch.tensor([financial_features], dtype=torch.float32).to(self.device)
            
            # El sentimiento a veces necesita ser una lista o tensor aparte dependiendo de tu hybrid_model
            sent_tensor = torch.tensor([[sentiment_score]], dtype=torch.float32).to(self.device)

            # 2. Inferencia (Sin calcular gradientes para ahorrar memoria)
            with torch.no_grad():
                # Pasamos los datos al modelo. 
                # NOTA: Ajusta los argumentos según tu definición en hybrid_model.py (forward)
                prediction = self.model(fin_tensor, sent_tensor)
                
            # 3. Post-procesamiento
            predicted_value = prediction.item() # Convertir tensor a float de Python

            # Lógica de interpretación (Opcional)
            recommendation = "MANTENER"
            if predicted_value > 0.05: recommendation = "COMPRAR"
            elif predicted_value < -0.05: recommendation = "VENDER"

            return {
                "ticker": ticker,
                "predicted_variation": round(predicted_value, 4),
                "recommendation": recommendation,
                "model_status": "trained" if os.path.exists(self.local_weights_path) else "random_weights"
            }

        except Exception as e:
            logger.error(f"❌ Error en predicción para {ticker}: {str(e)}")
            return {"error": "Prediction failed", "details": str(e)}