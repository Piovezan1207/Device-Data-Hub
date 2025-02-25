# from src.handler.mqttLoop import client
from src.handler.mqttLoop import sendRobotPosition
# import threading

import paho.mqtt.client as mqtt

BROKER = "10.83.146.40"  # Replace with your broker address
PORT = 1884
TOPIC = "projetoFinep/openLab_1.09/mir"



if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    sendRobotPosition(client)
    
    # sendPositions_thread = threading.Thread(target=sendRobotPosition, args=(client,))
    # sendPositions_thread.daemon = True
    # sendPositions_thread.start()
    
    # client.loop_forever()