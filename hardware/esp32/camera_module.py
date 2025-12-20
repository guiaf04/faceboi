# FaceBoi ESP32 - Módulo Câmera
# Controle da câmera ESP32-CAM

import camera
import time
from config import IMAGE_QUALITY, FRAME_SIZE, DEBUG

class Camera:
    """Controle da câmera ESP32-CAM"""
    
    # Tamanhos de frame disponíveis
    FRAME_SIZES = {
        'QQVGA': 0,   # 160x120
        'QQVGA2': 1,  # 128x160
        'QCIF': 2,    # 176x144
        'HQVGA': 3,   # 240x176
        'QVGA': 4,    # 320x240
        'CIF': 5,     # 400x296
        'VGA': 6,     # 640x480
        'SVGA': 7,    # 800x600
        'XGA': 8,     # 1024x768
        'SXGA': 9,    # 1280x1024
        'UXGA': 10,   # 1600x1200
    }
    
    def __init__(self, frame_size='SVGA', quality=12):
        """
        Inicializa a câmera
        
        Args:
            frame_size: Tamanho do frame (string ou int)
            quality: Qualidade JPEG (10-63, menor = melhor)
        """
        self.frame_size = frame_size
        self.quality = quality
        self.initialized = False
        
    def init(self):
        """Inicializa o hardware da câmera"""
        try:
            # Desinicializa se já estava inicializada
            try:
                camera.deinit()
            except:
                pass
            
            time.sleep_ms(100)
            
            # Inicializa a câmera
            # Parâmetros específicos para ESP32-CAM AI-Thinker
            camera.init(
                0,  # Modo JPEG
                d0=5, d1=18, d2=19, d3=21, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG,
                framesize=self._get_frame_size(),
                xclk_freq=20000000,
                href=23, vsync=25, reset=-1, pwdn=32,
                sioc=27, siod=26, xclk=0, pclk=22
            )
            
            # Configura qualidade
            camera.quality(self.quality)
            
            # Configurações adicionais
            camera.brightness(0)  # -2 a 2
            camera.contrast(0)    # -2 a 2
            camera.saturation(0)  # -2 a 2
            
            # Flip vertical/horizontal se necessário
            # camera.flip(1)
            # camera.mirror(1)
            
            self.initialized = True
            if DEBUG:
                print(f"[Camera] Inicializada - {self.frame_size}, qualidade {self.quality}")
            
            return True
            
        except Exception as e:
            print(f"[Camera] Erro na inicialização: {e}")
            self.initialized = False
            return False
    
    def _get_frame_size(self):
        """Retorna o código do tamanho do frame"""
        if isinstance(self.frame_size, int):
            return self.frame_size
        return self.FRAME_SIZES.get(self.frame_size.upper(), 7)  # Default SVGA
    
    def capture(self):
        """
        Captura uma foto
        
        Returns:
            bytes: Dados da imagem JPEG ou None em caso de erro
        """
        if not self.initialized:
            if not self.init():
                return None
        
        try:
            # Descarta primeiro frame (pode estar corrompido)
            camera.capture()
            time.sleep_ms(100)
            
            # Captura real
            img = camera.capture()
            
            if img:
                if DEBUG:
                    print(f"[Camera] Foto capturada: {len(img)} bytes")
                return img
            else:
                print("[Camera] Falha na captura")
                return None
                
        except Exception as e:
            print(f"[Camera] Erro na captura: {e}")
            return None
    
    def deinit(self):
        """Desinicializa a câmera"""
        try:
            camera.deinit()
            self.initialized = False
            if DEBUG:
                print("[Camera] Desinicializada")
        except:
            pass


def create_camera(frame_size=FRAME_SIZE, quality=IMAGE_QUALITY):
    """Factory function para criar câmera"""
    cam = Camera(frame_size=frame_size, quality=quality)
    if cam.init():
        return cam
    return None
