"""
FaceBoi - Servidor Flask
Recebe imagens da ESP32 e estima peso dos animais
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import HOST, PORT, DEBUG, UPLOAD_FOLDER, DATABASE_FILE, MODEL_PATH
from weight_model import get_estimator

# Inicializa Flask
app = Flask(__name__)
CORS(app)

# Cria diretórios necessários
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_FILE) if os.path.dirname(DATABASE_FILE) else 'data', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Inicializa estimador de peso
estimator = get_estimator(MODEL_PATH if os.path.exists(MODEL_PATH) else None)


def load_database():
    """Carrega banco de dados JSON"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {'cattle': {}, 'captures': []}


def save_database(db):
    """Salva banco de dados JSON"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(db, f, indent=2, default=str)


def save_image(rfid_tag, camera_position, image_bytes):
    """Salva imagem no disco"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{rfid_tag}_{camera_position}_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, 'wb') as f:
        f.write(image_bytes)
    
    return filepath


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'service': 'FaceBoi Server',
        'version': '1.0.0-mvp'
    })


@app.route('/api/capture', methods=['POST'])
def capture():
    """
    Endpoint principal - recebe captura da ESP32
    
    Payload esperado:
    {
        "device_id": "ESP32-CAM-001",
        "camera_position": "frontal",
        "rfid_tag": "A1B2C3D4",
        "image_base64": "...",
        "timestamp": 1234567890
    }
    """
    try:
        data = request.get_json()
        
        # Valida campos obrigatórios
        required = ['device_id', 'rfid_tag', 'image_base64']
        for field in required:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório ausente: {field}'
                }), 400
        
        # Extrai dados
        device_id = data['device_id']
        camera_position = data.get('camera_position', 'unknown')
        rfid_tag = data['rfid_tag']
        image_b64 = data['image_base64']
        timestamp = data.get('timestamp', datetime.now().timestamp())
        
        # Decodifica imagem
        try:
            image_bytes = base64.b64decode(image_b64)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Erro ao decodificar imagem: {e}'
            }), 400
        
        # Salva imagem
        image_path = save_image(rfid_tag, camera_position, image_bytes)
        
        # Processa imagem e estima peso
        result = estimator.process_image(image_bytes)
        
        # Carrega DB
        db = load_database()
        
        # Atualiza registro do animal
        if rfid_tag not in db['cattle']:
            db['cattle'][rfid_tag] = {
                'rfid': rfid_tag,
                'first_seen': datetime.now().isoformat(),
                'weights': [],
                'captures': []
            }
        
        cattle = db['cattle'][rfid_tag]
        cattle['last_seen'] = datetime.now().isoformat()
        
        # Registra captura
        capture_record = {
            'timestamp': datetime.now().isoformat(),
            'device_id': device_id,
            'camera_position': camera_position,
            'image_path': image_path
        }
        
        if result['success']:
            capture_record['estimated_weight'] = result['estimated_weight']
            capture_record['confidence'] = result.get('confidence', 0)
            capture_record['features'] = result.get('features', {})
            
            # Adiciona ao histórico de pesos
            cattle['weights'].append({
                'date': datetime.now().isoformat(),
                'weight': result['estimated_weight'],
                'confidence': result.get('confidence', 0)
            })
            
            # Mantém apenas últimos 100 registros
            cattle['weights'] = cattle['weights'][-100:]
        
        cattle['captures'].append(capture_record)
        cattle['captures'] = cattle['captures'][-50:]  # Últimas 50 capturas
        
        # Adiciona à lista geral de capturas
        db['captures'].append({
            'rfid_tag': rfid_tag,
            **capture_record
        })
        db['captures'] = db['captures'][-500:]  # Últimas 500 capturas
        
        # Salva DB
        save_database(db)
        
        # Prepara resposta
        response = {
            'success': True,
            'rfid_tag': rfid_tag,
            'device_id': device_id,
            'camera_position': camera_position,
            'image_saved': image_path
        }
        
        if result['success']:
            response['estimated_weight'] = result['estimated_weight']
            response['confidence'] = result.get('confidence', 0)
            response['features'] = result.get('features', {})
            
            # Calcula média dos últimos pesos
            recent_weights = [w['weight'] for w in cattle['weights'][-5:]]
            response['average_weight'] = round(sum(recent_weights) / len(recent_weights), 1)
        else:
            response['weight_error'] = result.get('error', 'Erro desconhecido')
        
        print(f"[Capture] {rfid_tag} | {camera_position} | Peso: {response.get('estimated_weight', 'N/A')} kg")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/cattle', methods=['GET'])
def list_cattle():
    """Lista todos os animais registrados"""
    db = load_database()
    
    cattle_list = []
    for rfid, data in db['cattle'].items():
        cattle_info = {
            'rfid': rfid,
            'first_seen': data.get('first_seen'),
            'last_seen': data.get('last_seen'),
            'total_captures': len(data.get('captures', []))
        }
        
        # Último peso
        weights = data.get('weights', [])
        if weights:
            cattle_info['last_weight'] = weights[-1]['weight']
            cattle_info['last_weight_date'] = weights[-1]['date']
            
            # Variação de peso
            if len(weights) >= 2:
                cattle_info['weight_change'] = round(weights[-1]['weight'] - weights[-2]['weight'], 1)
        
        cattle_list.append(cattle_info)
    
    return jsonify({
        'success': True,
        'count': len(cattle_list),
        'cattle': cattle_list
    })


@app.route('/api/cattle/<rfid_tag>', methods=['GET'])
def get_cattle(rfid_tag):
    """Retorna detalhes de um animal específico"""
    db = load_database()
    
    if rfid_tag not in db['cattle']:
        return jsonify({
            'success': False,
            'error': 'Animal não encontrado'
        }), 404
    
    cattle = db['cattle'][rfid_tag]
    
    return jsonify({
        'success': True,
        'cattle': cattle
    })


@app.route('/api/captures/recent', methods=['GET'])
def recent_captures():
    """Retorna capturas recentes"""
    limit = request.args.get('limit', 20, type=int)
    
    db = load_database()
    captures = db.get('captures', [])[-limit:]
    captures.reverse()  # Mais recentes primeiro
    
    return jsonify({
        'success': True,
        'count': len(captures),
        'captures': captures
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    """Estatísticas gerais"""
    db = load_database()
    
    total_cattle = len(db.get('cattle', {}))
    total_captures = len(db.get('captures', []))
    
    # Calcula peso médio
    all_weights = []
    for cattle in db.get('cattle', {}).values():
        weights = cattle.get('weights', [])
        if weights:
            all_weights.append(weights[-1]['weight'])
    
    avg_weight = round(sum(all_weights) / len(all_weights), 1) if all_weights else 0
    
    return jsonify({
        'success': True,
        'stats': {
            'total_cattle': total_cattle,
            'total_captures': total_captures,
            'average_weight': avg_weight,
            'weights_count': len(all_weights)
        }
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("    FaceBoi Server - MVP")
    print("="*50)
    print(f"Host: {HOST}:{PORT}")
    print(f"Debug: {DEBUG}")
    print(f"Uploads: {UPLOAD_FOLDER}")
    print(f"Database: {DATABASE_FILE}")
    print("="*50 + "\n")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
