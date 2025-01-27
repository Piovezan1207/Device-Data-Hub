import paho.mqtt.client as mqtt
import json

from ..DTO.RobotDTO import RobotDTO

from ..controller.RobotController import RobotController
from ..External.yaskawaHC10Connection import yaskawaHC10Connection
from ..adapter.YaskawaRobotAdapter import YaskawaRobotAdapter

from ..DTO.RequestDTO import RequestDTO

from ..controller.RequestController import RequestController
from ..adapter.RequestDashboardAdapter import RequestDashboardAdapter
import json

from dotenv import load_dotenv
import os

load_dotenv()

BROKER_IP=os.getenv("BROKER_IP")
BROKER_PORT=int(os.getenv("BROKER_PORT"))
BROKER_USER=os.getenv("BROKER_USER")
BROKER_PASSWORD=os.getenv("BROKER_PASSWORD")

ROBOT_POSITION_TOPIC=os.getenv("ROBOT_POSITION_TOPIC")
ROBOT_POSITION_TOPIC_CALLBACK=os.getenv("ROBOT_POSITION_TOPIC_CALLBACK")
ROBOT_IP=os.getenv("ROBOT_IP")
ROBOT_PORT=int(os.getenv("ROBOT_PORT"))
ROBOT_AXIS_NUMBER=int(os.getenv("ROBOT_AXIS_NUMBER"))
ROBOT_NUMBER=os.getenv("ROBOT_NUMBER")
ROBOT_DESCRIPTION=os.getenv("ROBOT_DESCRIPTION")
ROBOT_BRAND=os.getenv("ROBOT_BRAND")
DASHBOARD_TOPIC=os.getenv("DASHBOARD_TOPIC")

print(BROKER_IP,
BROKER_PORT,
BROKER_USER,
BROKER_PASSWORD,
ROBOT_POSITION_TOPIC,
ROBOT_POSITION_TOPIC_CALLBACK,
ROBOT_IP,
ROBOT_PORT,
ROBOT_AXIS_NUMBER,
ROBOT_NUMBER,
ROBOT_DESCRIPTION,
ROBOT_BRAND,
DASHBOARD_TOPIC)


#Função que será chamada no momento que a conexão com o broker for feita
def on_connect(client, userdata, flags, rc):    
    print("Connected with result code "+str(rc))    
    print(ROBOT_POSITION_TOPIC_CALLBACK)
    client.subscribe(ROBOT_POSITION_TOPIC_CALLBACK) #Se inscreve em um tópico
#Função que vai ser chamada sxempre que chegar uma mensagem do tópico que está inscrito

def on_message(client, userdata, msg):    
    # print(msg.topic+" "+str(msg.payload)) 
    mensagem = msg.payload
    client.publish(DASHBOARD_TOPIC, testLatency(mensagem))
    # print()

def testLatency(payload):
    
    jsonPayload = json.loads(payload)
    
    newRequest = RequestDTO(1, jsonPayload["request_timestemp"], jsonPayload["robot_fun_process_time"])
    
    requestAdapter = RequestDashboardAdapter()
    
    DtInfo = RequestController.calculateTime(newRequest, requestAdapter)
    
    return(DtInfo)


def sendRobotPosition(client):
    # newRobot = RobotDTO("Yaskawa", "Robo de montagem do lab 10", 6)
    newRobot = RobotDTO(ROBOT_BRAND, ROBOT_DESCRIPTION, ROBOT_AXIS_NUMBER)

    robotConnector = yaskawaHC10Connection(ROBOT_IP, ROBOT_PORT)
    robotAdapter = YaskawaRobotAdapter()

    while True:
        try:
            robot_information = RobotController.getRobotInfo(newRobot, robotConnector, robotAdapter)
        except:
            pass
        client.publish(ROBOT_POSITION_TOPIC , robot_information)
    
    return robot_information

client = mqtt.Client() #Cria um cliente MQTT
client.on_connect = on_connect #Define qual a função que será chamada quando se concetar ao broker
client.on_message = on_message #Define qual a função que será chamada quando receber uma mensagem
print("Conectando...")
client.username_pw_set(BROKER_USER, BROKER_PASSWORD) #Configura o login e senha do broker (apenas é necessário se o broker tiver senha)
# client.connect("broker.hubsenai.com", 1883, 60) #Se conecta a um broker
client.connect(BROKER_IP, BROKER_PORT, 60) #Se conecta a um broker







