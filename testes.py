import socket
import struct
import time

# Configurações do dispositivo
DEVICE_IP = "10.83.146.63"  # IP do dispositivo
DEVICE_PORT = 10040         # Porta do dispositivo
PACKET = b'YERC \x00\x00\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999u\x00\x01\x00\x00\x01\x00\x00'

def process_response(data):
    """Processa a resposta e extrai os inteiros da posição."""
    payload = data[20:]  # Ignorar os primeiros 20 bytes
    return [struct.unpack('<i', payload[i:i+4])[0] for i in range(0, len(payload), 4) if i + 4 <= len(payload)]

def get_position(sock):
    """Envia o pacote e retorna a posição processada."""
    start_time = time.perf_counter()
    sock.sendto(PACKET, (DEVICE_IP, DEVICE_PORT))
    response, _ = sock.recvfrom(1024)  # Tamanho máximo esperado da resposta
    latency = (time.perf_counter() - start_time) * 1000  # Latência em ms
    position = process_response(response)
    return position, latency

# Criar o socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(1)  # Timeout de 1 segundo
    
    print(f"Conectado ao dispositivo {DEVICE_IP}:{DEVICE_PORT}.")
    
    try:
        # Obter posição e latência
        position, latency = get_position(sock)
        print(f"Posição: {position}, Latência: {latency:.3f} ms")
    except socket.timeout:
        print("Timeout: Nenhuma resposta recebida.")
        

