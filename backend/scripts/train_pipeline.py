import sys
import os

# Truco para que Python encuentre la carpeta 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trainer import TrainingService

if __name__ == "__main__":
    trainer = TrainingService()
    trainer.train_model()