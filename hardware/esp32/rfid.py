# FaceBoi ESP32 - Módulo RFID MFRC522
# Biblioteca simplificada para leitura de tags RFID

from machine import Pin, SoftSPI
import time

class MFRC522:
    """
    Driver simplificado para MFRC522
    Baseado em: https://github.com/wendlers/micropython-mfrc522
    """
    
    # Comandos
    REQIDL = 0x26
    REQALL = 0x52
    AUTHENT1A = 0x60
    AUTHENT1B = 0x61
    
    # Registradores
    CommandReg = 0x01
    CommIEnReg = 0x02
    CommIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    ModeReg = 0x11
    TxControlReg = 0x14
    TxASKReg = 0x15
    CRCResultRegL = 0x22
    CRCResultRegH = 0x21
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    
    # Comandos PCD
    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03
    
    # Comandos PICC
    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SElECTTAG = 0x93
    PICC_READ = 0x30
    
    def __init__(self, sck=13, mosi=12, miso=14, cs=15, rst=2):
        """Inicializa o leitor RFID"""
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)
        
        self.spi = SoftSPI(
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=Pin(sck),
            mosi=Pin(mosi),
            miso=Pin(miso)
        )
        
        self.cs.value(1)
        self.init()
    
    def _write(self, reg, val):
        """Escreve em um registrador"""
        self.cs.value(0)
        self.spi.write(bytes([(reg << 1) & 0x7E, val]))
        self.cs.value(1)
    
    def _read(self, reg):
        """Lê de um registrador"""
        self.cs.value(0)
        self.spi.write(bytes([((reg << 1) & 0x7E) | 0x80]))
        val = self.spi.read(1)
        self.cs.value(1)
        return val[0]
    
    def _set_bit(self, reg, mask):
        """Define bits em um registrador"""
        self._write(reg, self._read(reg) | mask)
    
    def _clear_bit(self, reg, mask):
        """Limpa bits em um registrador"""
        self._write(reg, self._read(reg) & (~mask))
    
    def init(self):
        """Inicializa o módulo MFRC522"""
        self._write(self.TModeReg, 0x8D)
        self._write(self.TPrescalerReg, 0x3E)
        self._write(self.TReloadRegL, 30)
        self._write(self.TReloadRegH, 0)
        self._write(self.TxASKReg, 0x40)
        self._write(self.ModeReg, 0x3D)
        self.antenna_on()
    
    def antenna_on(self):
        """Liga a antena"""
        val = self._read(self.TxControlReg)
        if not (val & 0x03):
            self._set_bit(self.TxControlReg, 0x03)
    
    def antenna_off(self):
        """Desliga a antena"""
        self._clear_bit(self.TxControlReg, 0x03)
    
    def reset(self):
        """Reset do módulo"""
        self._write(self.CommandReg, self.PCD_RESETPHASE)
    
    def request(self, mode=PICC_REQIDL):
        """Requisita tag"""
        self._write(self.BitFramingReg, 0x07)
        status, data = self._tocard(self.PCD_TRANSCEIVE, [mode])
        if status != 0 or len(data) != 2:
            return None
        return data
    
    def anticoll(self):
        """Anti-colisão - obtém UID"""
        self._write(self.BitFramingReg, 0x00)
        status, data = self._tocard(self.PCD_TRANSCEIVE, [self.PICC_ANTICOLL, 0x20])
        if status != 0 or len(data) != 5:
            return None
        # Verifica checksum
        if data[0] ^ data[1] ^ data[2] ^ data[3] != data[4]:
            return None
        return data[:4]
    
    def _tocard(self, cmd, data):
        """Comunica com o cartão"""
        back_data = []
        irq_en = 0x00
        wait_irq = 0x00
        
        if cmd == self.PCD_AUTHENT:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == self.PCD_TRANSCEIVE:
            irq_en = 0x77
            wait_irq = 0x30
        
        self._write(self.CommIEnReg, irq_en | 0x80)
        self._clear_bit(self.CommIrqReg, 0x80)
        self._set_bit(self.FIFOLevelReg, 0x80)
        self._write(self.CommandReg, self.PCD_IDLE)
        
        for byte in data:
            self._write(self.FIFODataReg, byte)
        
        self._write(self.CommandReg, cmd)
        
        if cmd == self.PCD_TRANSCEIVE:
            self._set_bit(self.BitFramingReg, 0x80)
        
        # Aguarda resposta
        i = 2000
        while True:
            n = self._read(self.CommIrqReg)
            i -= 1
            if i == 0 or (n & wait_irq):
                break
        
        self._clear_bit(self.BitFramingReg, 0x80)
        
        if i == 0:
            return -1, []
        
        if self._read(self.ErrorReg) & 0x1B:
            return -1, []
        
        if n & irq_en & 0x01:
            return -2, []
        
        if cmd == self.PCD_TRANSCEIVE:
            n = self._read(self.FIFOLevelReg)
            for _ in range(n):
                back_data.append(self._read(self.FIFODataReg))
        
        return 0, back_data
    
    def read_card(self):
        """
        Tenta ler uma tag RFID
        Retorna: string com UID hex ou None
        """
        if self.request() is None:
            return None
        
        uid = self.anticoll()
        if uid is None:
            return None
        
        # Converte para string hexadecimal
        uid_hex = ''.join(['{:02X}'.format(b) for b in uid])
        return uid_hex


def create_rfid(sck=13, mosi=12, miso=14, cs=15, rst=2):
    """Factory function para criar leitor RFID"""
    try:
        rfid = MFRC522(sck=sck, mosi=mosi, miso=miso, cs=cs, rst=rst)
        print("[RFID] Inicializado com sucesso")
        return rfid
    except Exception as e:
        print(f"[RFID] Erro na inicialização: {e}")
        return None
