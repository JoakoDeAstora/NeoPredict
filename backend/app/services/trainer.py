import torch
import torch.nn as nn
import torch.optim as optim
import os
from google.cloud import storage
from app.models.hybrid_model import FinancialNeuralNet # Asumiendo que tu modelo se llama así
# from app.utils.db import get_db_connection # Tu función para conectar a BD

class TrainingService:
    def __init__(self):
        self.bucket_name = "neopredict-weights" # CREA ESTE BUCKET EN GCP
        self.weights_file = "model_weights.pth"
        self.local_path = f"/tmp/{self.weights_file}" # Usamos /tmp en Cloud Run

    def train_model(self):
        print("🧠 Iniciando entrenamiento...")
        
        # 1. OBTENER DATOS (Simulado por ahora)
        # Aquí deberías hacer una query a tu BD para sacar X (inputs) e y (target)
        # X_train, y_train = data_service.get_training_data()
        
        # Simulación de datos para que el código no falle si no tienes datos aún
        X_train = torch.randn(10, 50) # 10 ejemplos, 50 features
        y_train = torch.randn(10, 1)  # 10 objetivos
        
        # 2. INICIALIZAR MODELO
        model = FinancialNeuralNet() # Asegúrate de pasar los parámetros correctos
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        # 3. CICLO DE ENTRENAMIENTO (Epochs)
        model.train()
        for epoch in range(50): # 50 épocas de ejemplo
            optimizer.zero_grad()
            outputs = model(X_train) # Ajustar según los inputs de tu modelo híbrido
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
            
        print("✅ Entrenamiento finalizado.")

        # 4. GUARDAR PESOS LOCALMENTE
        torch.save(model.state_dict(), self.local_path)
        
        # 5. SUBIR A GOOGLE CLOUD STORAGE
        self._upload_to_gcp()

    def _upload_to_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.weights_file)
            blob.upload_from_filename(self.local_path)
            print(f"☁️ Pesos subidos exitosamente al bucket: {self.bucket_name}")
        except Exception as e:
            print(f"❌ Error subiendo a GCP (¿Tienes las credenciales?): {e}")