# FaceBoi Server - Configurações
import os
from dotenv import load_dotenv

load_dotenv()

# Servidor
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Armazenamento de imagens
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Modelo de peso
MODEL_PATH = os.getenv('MODEL_PATH', 'models/weight_model.pkl')
MIN_IMAGES_FOR_ESTIMATION = 1  # Mínimo de imagens para estimar peso

# Banco de dados (para MVP, usamos JSON simples)
DATABASE_FILE = os.getenv('DATABASE_FILE', 'data/cattle_db.json')
