# FaceBoi - Hardware MVP

## Componentes Necessários

### Microcontrolador
- **ESP32-CAM** (AI-Thinker) - já inclui câmera OV2640
  - Alternativa: ESP32 + módulo câmera separado

### Leitor RFID
- **MFRC522** (13.56 MHz) ou **RDM6300** (125 kHz)
  - Recomendado: MFRC522 para maior alcance e velocidade

### Alimentação
- Painel Solar 6V 2W (opcional para campo)
- Bateria Li-Ion 18650 3.7V
- Módulo TP4056 para carga
- Regulador de tensão 3.3V

### Estrutura
- Corredor de passagem para o gado
- Suporte para 4 câmeras (frontal, laterais, superior)
- Antena RFID no piso ou lateral

## Pinagem ESP32-CAM + MFRC522

```
ESP32-CAM    MFRC522
---------    -------
3.3V    -->  VCC
GND     -->  GND
GPIO13  -->  SCK
GPIO12  -->  MOSI
GPIO14  -->  MISO
GPIO15  -->  SDA (SS)
GPIO2   -->  RST
```

**Nota:** A ESP32-CAM tem pinos limitados. Para produção, considere usar ESP32 com módulo de câmera externo.

## Fluxo de Operação

1. Animal passa pelo corredor
2. RFID detecta o brinco e lê o ID
3. ESP32 dispara as 4 câmeras (ou sequencialmente com 1 câmera)
4. Imagens são enviadas ao servidor via WiFi
5. Servidor processa com ML e estima o peso
6. Dados são salvos no banco e disponibilizados no dashboard

## Arquivos

- `esp32/boot.py` - Configuração inicial
- `esp32/main.py` - Código principal
- `esp32/config.py` - Configurações WiFi e servidor
- `esp32/rfid.py` - Biblioteca RFID
- `esp32/camera.py` - Controle da câmera
- `server/app.py` - Servidor Flask
- `server/weight_model.py` - Modelo de estimativa de peso
- `server/requirements.txt` - Dependências Python
