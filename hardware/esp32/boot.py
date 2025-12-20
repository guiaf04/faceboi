# FaceBoi ESP32 - Boot
# Executa na inicialização

import network
import time
from config import WIFI_SSID, WIFI_PASSWORD, DEBUG

def connect_wifi():
    """Conecta ao WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        if DEBUG:
            print("[WiFi] Já conectado:", wlan.ifconfig())
        return True
    
    print(f"[WiFi] Conectando a {WIFI_SSID}...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Aguarda conexão (máximo 20 segundos)
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        if DEBUG:
            print(f"[WiFi] Aguardando... {timeout}s")
    
    if wlan.isconnected():
        print("[WiFi] Conectado!")
        print("[WiFi] IP:", wlan.ifconfig()[0])
        return True
    else:
        print("[WiFi] Falha na conexão!")
        return False

# Conecta ao WiFi na inicialização
connect_wifi()
