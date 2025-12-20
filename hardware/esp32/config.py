# FaceBoi ESP32 - Configurações
# Edite este arquivo com suas credenciais

# WiFi
WIFI_SSID = "SuaRedeWiFi"
WIFI_PASSWORD = "SuaSenhaWiFi"

# Servidor FaceBoi
SERVER_URL = "http://192.168.1.100:5000"
API_ENDPOINT = "/api/capture"

# Identificação do dispositivo
DEVICE_ID = "ESP32-CAM-001"
CAMERA_POSITION = "frontal"  # frontal, lateral_esq, lateral_dir, superior

# RFID
RFID_ENABLED = True

# Configurações de captura
CAPTURE_DELAY_MS = 500  # Delay entre detecção RFID e foto
IMAGE_QUALITY = 12  # 10-63, menor = melhor qualidade
FRAME_SIZE = 10  # FRAMESIZE_UXGA=13, SVGA=10, VGA=8, CIF=6

# Debug
DEBUG = True
