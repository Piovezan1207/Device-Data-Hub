from src.handler.mqttLoop import client
from src.handler.mqttLoop import sendRobotPosition
import threading

if __name__ == "__main__":
    sendPositions_thread = threading.Thread(target=sendRobotPosition, args=(client,))
    sendPositions_thread.daemon = True
    sendPositions_thread.start()
    
    client.loop_forever()