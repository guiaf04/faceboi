# FaceBoi ESP32 - Programa Principal
# Lê RFID, captura foto e envia ao servidor

import time
import gc
import urequests
import ubinascii
import json
from machine import Pin, reset

from config import (
    SERVER_URL, API_ENDPOINT, DEVICE_ID, CAMERA_POSITION,
    RFID_ENABLED, CAPTURE_DELAY_MS, DEBUG
)
from rfid import create_rfid
from camera_module import create_camera

# LED indicador (GPIO 4 na ESP32-CAM)
led = Pin(4, Pin.OUT)


def blink_led(times=1, delay=200):
    """Pisca o LED indicador"""
    for _ in range(times):
        led.value(1)
        time.sleep_ms(delay)
        led.value(0)
        time.sleep_ms(delay)


def send_to_server(rfid_tag, image_data):
    """
    Envia dados para o servidor
    
    Args:
        rfid_tag: ID do RFID lido
        image_data: bytes da imagem JPEG
    
    Returns:
        dict: Resposta do servidor ou None em caso de erro
    """
    url = f"{SERVER_URL}{API_ENDPOINT}"
    
    try:
        # Converte imagem para base64
        image_b64 = ubinascii.b2a_base64(image_data).decode('utf-8').strip()
        
        # Monta payload
        payload = {
            "device_id": DEVICE_ID,
            "camera_position": CAMERA_POSITION,
            "rfid_tag": rfid_tag,
            "image_base64": image_b64,
            "timestamp": time.time()
        }
        
        if DEBUG:
            print(f"[Server] Enviando para {url}")
            print(f"[Server] RFID: {rfid_tag}, Imagem: {len(image_data)} bytes")
        
        # Envia requisição POST
        headers = {"Content-Type": "application/json"}
        response = urequests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if DEBUG:
                print(f"[Server] Sucesso: {result}")
            response.close()
            return result
        else:
            print(f"[Server] Erro HTTP {response.status_code}")
            response.close()
            return None
            
    except Exception as e:
        print(f"[Server] Erro ao enviar: {e}")
        return None


def process_detection(rfid_tag, cam):
    """
    Processa uma detecção de RFID
    
    Args:
        rfid_tag: ID do RFID detectado
        cam: Instância da câmera
    """
    print(f"\n{'='*40}")
    print(f"[RFID] Tag detectada: {rfid_tag}")
    
    # Indica detecção
    blink_led(2, 100)
    
    # Aguarda o animal se posicionar
    time.sleep_ms(CAPTURE_DELAY_MS)
    
    # Captura foto
    print("[Camera] Capturando...")
    image = cam.capture()
    
    if image is None:
        print("[Camera] Falha na captura!")
        blink_led(5, 50)  # Erro
        return
    
    # Envia ao servidor
    print("[Server] Enviando dados...")
    result = send_to_server(rfid_tag, image)
    
    # Libera memória
    del image
    gc.collect()
    
    if result:
        # Sucesso - mostra peso estimado se disponível
        if 'estimated_weight' in result:
            print(f"[Peso] Estimativa: {result['estimated_weight']} kg")
        blink_led(1, 500)  # Sucesso
    else:
        blink_led(3, 100)  # Erro no envio
    
    print(f"{'='*40}\n")


def main():
    """Loop principal"""
    print("\n" + "="*50)
    print("    FaceBoi - Sistema de Pesagem Inteligente")
    print("="*50)
    print(f"Dispositivo: {DEVICE_ID}")
    print(f"Câmera: {CAMERA_POSITION}")
    print(f"Servidor: {SERVER_URL}")
    print("="*50 + "\n")
    
    # Inicializa componentes
    print("[Init] Inicializando câmera...")
    cam = create_camera()
    if cam is None:
        print("[ERRO] Falha ao inicializar câmera!")
        blink_led(10, 100)
        time.sleep(5)
        reset()
    
    rfid = None
    if RFID_ENABLED:
        print("[Init] Inicializando RFID...")
        rfid = create_rfid()
        if rfid is None:
            print("[AVISO] RFID não disponível, modo manual ativado")
    
    print("\n[Sistema] Pronto! Aguardando detecções...\n")
    blink_led(3, 200)  # Indica pronto
    
    # Variáveis de controle
    last_tag = None
    last_detection_time = 0
    detection_cooldown = 5000  # 5 segundos entre detecções do mesmo tag
    
    # Loop principal
    while True:
        try:
            current_time = time.ticks_ms()
            
            # Tenta ler RFID
            if rfid:
                tag = rfid.read_card()
                
                if tag:
                    # Verifica cooldown para evitar leituras duplicadas
                    if tag != last_tag or time.ticks_diff(current_time, last_detection_time) > detection_cooldown:
                        process_detection(tag, cam)
                        last_tag = tag
                        last_detection_time = current_time
            
            # Pequeno delay para não sobrecarregar
            time.sleep_ms(100)
            
            # Coleta de lixo periódica
            if time.ticks_diff(current_time, last_detection_time) > 30000:
                gc.collect()
                
        except KeyboardInterrupt:
            print("\n[Sistema] Interrompido pelo usuário")
            break
            
        except Exception as e:
            print(f"[ERRO] {e}")
            blink_led(5, 50)
            time.sleep(1)
    
    # Cleanup
    if cam:
        cam.deinit()
    print("[Sistema] Encerrado")


# Executa
if __name__ == "__main__":
    main()
