"""
FaceBoi - Modelo de Estimativa de Peso
MVP usando dimensões extraídas da imagem do animal

Este é um modelo simplificado para demonstração.
Em produção, seria treinado com milhares de imagens reais.
"""

import os
import pickle
import numpy as np
from PIL import Image
import cv2
import io

class WeightEstimator:
    """
    Estimador de peso baseado em dimensões do animal na imagem.
    
    Abordagem MVP:
    1. Detecta contorno do animal (segmentação simples)
    2. Extrai métricas: área, perímetro, largura, altura
    3. Usa regressão para estimar peso
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.model_path = model_path
        
        # Parâmetros de calibração (ajustados empiricamente)
        # Em produção, estes seriam aprendidos com dados reais
        self.calibration = {
            'area_factor': 0.0012,      # kg por pixel² de área
            'length_factor': 0.85,       # kg por pixel de comprimento
            'width_factor': 0.65,        # kg por pixel de largura
            'base_weight': 150,          # Peso base mínimo (kg)
            'max_weight': 800,           # Peso máximo (kg)
        }
        
        # Carrega modelo treinado se existir
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def preprocess_image(self, image_bytes):
        """
        Pré-processa a imagem para análise
        
        Args:
            image_bytes: bytes da imagem JPEG
        
        Returns:
            numpy array: Imagem processada
        """
        # Converte bytes para imagem
        image = Image.open(io.BytesIO(image_bytes))
        image = np.array(image)
        
        # Converte para BGR se necessário (OpenCV usa BGR)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        return image
    
    def segment_animal(self, image):
        """
        Segmenta o animal do fundo da imagem
        
        Args:
            image: numpy array da imagem BGR
        
        Returns:
            tuple: (máscara binária, contorno principal)
        """
        # Converte para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplica blur para reduzir ruído
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Threshold adaptativo
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Operações morfológicas para limpar
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Encontra contornos
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return None, None
        
        # Pega o maior contorno (assumindo que é o animal)
        main_contour = max(contours, key=cv2.contourArea)
        
        # Cria máscara
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [main_contour], -1, 255, -1)
        
        return mask, main_contour
    
    def extract_features(self, image, contour):
        """
        Extrai características do animal para estimativa de peso
        
        Args:
            image: numpy array da imagem
            contour: contorno do animal
        
        Returns:
            dict: Características extraídas
        """
        if contour is None:
            return None
        
        # Área do contorno
        area = cv2.contourArea(contour)
        
        # Perímetro
        perimeter = cv2.arcLength(contour, True)
        
        # Bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Retângulo rotacionado (melhor ajuste)
        rect = cv2.minAreaRect(contour)
        (cx, cy), (width, height), angle = rect
        
        # Garante que width > height (comprimento > largura)
        if width < height:
            width, height = height, width
        
        # Elipse ajustada (se contorno tem pontos suficientes)
        ellipse_area = 0
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            ellipse_area = np.pi * (ellipse[1][0] / 2) * (ellipse[1][1] / 2)
        
        # Convexidade
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0
        
        # Proporção da imagem ocupada pelo animal
        image_area = image.shape[0] * image.shape[1]
        fill_ratio = area / image_area
        
        features = {
            'area': area,
            'perimeter': perimeter,
            'width': width,
            'height': height,
            'length': max(width, height),  # Comprimento do animal
            'bbox_width': w,
            'bbox_height': h,
            'aspect_ratio': width / height if height > 0 else 0,
            'solidity': solidity,
            'fill_ratio': fill_ratio,
            'ellipse_area': ellipse_area
        }
        
        return features
    
    def estimate_weight(self, features):
        """
        Estima o peso baseado nas características
        
        Args:
            features: dict com características extraídas
        
        Returns:
            float: Peso estimado em kg
        """
        if features is None:
            return None
        
        # Se temos modelo treinado, usa ele
        if self.model is not None:
            return self._predict_with_model(features)
        
        # Caso contrário, usa fórmula empírica (MVP)
        return self._empirical_estimation(features)
    
    def _empirical_estimation(self, features):
        """
        Estimativa empírica de peso (fórmula simplificada)
        
        Baseada em correlações conhecidas entre dimensões e peso de bovinos.
        Esta é uma aproximação para MVP.
        """
        cal = self.calibration
        
        # Normaliza área para escala típica de imagem
        # Assume imagem de ~800x600 pixels
        normalized_area = features['area'] / 10000
        
        # Comprimento e largura normalizados
        length = features['length'] / 100
        width = features['height'] / 100
        
        # Fórmula empírica:
        # Peso = base + (área * fator_área) + (comprimento * fator_comp) + (largura * fator_larg)
        weight = (
            cal['base_weight'] +
            normalized_area * cal['area_factor'] * 1000 +
            length * cal['length_factor'] * 10 +
            width * cal['width_factor'] * 10
        )
        
        # Ajuste por proporção (animais mais "preenchidos" são mais pesados)
        weight *= (0.8 + features['solidity'] * 0.4)
        
        # Limita ao range válido
        weight = max(cal['base_weight'], min(cal['max_weight'], weight))
        
        return round(weight, 1)
    
    def _predict_with_model(self, features):
        """Predição usando modelo ML treinado"""
        feature_vector = np.array([
            features['area'],
            features['perimeter'],
            features['length'],
            features['height'],
            features['aspect_ratio'],
            features['solidity'],
            features['fill_ratio']
        ]).reshape(1, -1)
        
        weight = self.model.predict(feature_vector)[0]
        return round(float(weight), 1)
    
    def process_image(self, image_bytes):
        """
        Processa imagem completa e retorna estimativa de peso
        
        Args:
            image_bytes: bytes da imagem JPEG
        
        Returns:
            dict: Resultado com peso estimado e features
        """
        try:
            # Pré-processa
            image = self.preprocess_image(image_bytes)
            
            # Segmenta animal
            mask, contour = self.segment_animal(image)
            
            if contour is None:
                return {
                    'success': False,
                    'error': 'Não foi possível detectar o animal na imagem'
                }
            
            # Extrai características
            features = self.extract_features(image, contour)
            
            # Estima peso
            weight = self.estimate_weight(features)
            
            return {
                'success': True,
                'estimated_weight': weight,
                'confidence': 0.75,  # MVP: confiança fixa
                'features': {
                    'area': int(features['area']),
                    'length': round(features['length'], 1),
                    'width': round(features['height'], 1),
                    'aspect_ratio': round(features['aspect_ratio'], 2)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_model(self, path):
        """Salva modelo treinado"""
        if self.model is not None:
            with open(path, 'wb') as f:
                pickle.dump(self.model, f)
    
    def load_model(self, path):
        """Carrega modelo treinado"""
        try:
            with open(path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"[WeightModel] Modelo carregado: {path}")
        except Exception as e:
            print(f"[WeightModel] Erro ao carregar modelo: {e}")
            self.model = None


# Singleton para uso no servidor
_estimator = None

def get_estimator(model_path=None):
    """Retorna instância singleton do estimador"""
    global _estimator
    if _estimator is None:
        _estimator = WeightEstimator(model_path)
    return _estimator
