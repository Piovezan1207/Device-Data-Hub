from ..interfaces.externalInterfaces import RobotExternalInterface
import socket
import struct

# Configurações do dispositivo
# DEVICE_IP = "10.83.146.64"  # IP do dispositivo
# DEVICE_PORT = 10040         # Porta do dispositivo
PACKET = b'YERC \x00\x00\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999u\x00\x01\x00\x00\x01\x00\x00'

s_ratio = 2671.3
l_ratio = 2671.3
u_ratio = 2347.4
r_ratio = 1619.1
b_ratio = 1619.2
t_ratio = 1619.1

deg2pulse_ratio = (s_ratio, l_ratio, u_ratio, r_ratio, b_ratio, t_ratio)
pulse2deg_ratio = tuple((d2p**(-1)) for d2p in deg2pulse_ratio)

class yaskawaHC10Connection(RobotExternalInterface):
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port

    def getRobotPosition(self) -> list:
        position = self.getPosition()
        return position

    def getClawStatus(self) -> int:
        return 1
        pass
    
    def process_response(self, data):
        """Processa a resposta e extrai os inteiros da posição."""
        payload = data[20:]  # Ignorar os primeiros 20 bytes
        response = [struct.unpack('<i', payload[i:i+4])[0] for i in range(0, len(payload), 4) if i + 4 <= len(payload)]
        robotPosition = response[8:]
        
        position_angles = list(round(p * p2d, 3) for p, p2d in zip(robotPosition, pulse2deg_ratio))
        
        return position_angles

    def sendPackage(self, sock):
        """Envia o pacote e retorna a posição processada."""
        sock.sendto(PACKET, (self._ip, self._port))
        response, _ = sock.recvfrom(1024)  # Tamanho máximo esperado da resposta
        position = self.process_response(response)
        return position

    def getPosition(self):
        # Criar o socket UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1)  # Timeout de 1 segundo
            try:
                # Obter posição e latência
                position = self.sendPackage(sock)
                return position
            except socket.timeout:
                print("Robot socket timeout: Nenhuma resposta recebida do robô em 1 segundo.")


