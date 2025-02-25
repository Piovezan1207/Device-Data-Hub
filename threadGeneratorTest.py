import paho.mqtt.client as mqtt
import json

from src.robot.pkg.DTO.RobotDTO import RobotDTO


from src.robot.adapters.controller.RobotController import RobotController

from src.robot.External.integrations.yaskawaHC10Connection import yaskawaHC10Connection
from src.robot.External.integrations.yaskawaGP8Connection import yaskawaGP8Connection
from src.robot.adapters.presenter.YaskawaRobotAdapter import YaskawaRobotAdapter

from src.robot.External.integrations.MIRConnection import MIRConnection
from src.robot.adapters.presenter.MirAdapter import MirAdapter

from src.robot.pkg.DTO.RequestDTO import RequestDTO

from src.robot.adapters.controller.RequestController import RequestController
from src.robot.adapters.presenter.RequestDashboardAdapter import RequestDashboardAdapter
import json

import threading


def testLatency(payload):
    jsonPayload = json.loads(payload)
    newRequest = RequestDTO(1, jsonPayload["request_timestemp"], jsonPayload["robot_fun_process_time"])
    requestAdapter = RequestDashboardAdapter()
    DtInfo = RequestController.calculateTime(newRequest, requestAdapter)
    return(DtInfo)

def sendRobotPosition(client, 
                      ROBOT_BRAND, 
                      ROBOT_DESCRIPTION, 
                      ROBOT_AXIS_NUMBER, 
                      ROBOT_POSITION_TOPIC, 
                      ROBOT_PASSWORD,
                      robotConnector,
                        robotAdapter
                      ):
    newRobot = RobotDTO(ROBOT_BRAND, ROBOT_DESCRIPTION, ROBOT_AXIS_NUMBER)
    while True:
        try:
            robot_information = RobotController.getRobotInfo(newRobot, robotConnector, robotAdapter)
            if client.is_connected():
                client.publish(ROBOT_POSITION_TOPIC , robot_information)
        except:
            pass


class MinhaThread(threading.Thread):
    def __init__(self, 
                 client, 
                ROBOT_BRAND, 
                ROBOT_DESCRIPTION, 
                ROBOT_AXIS_NUMBER, 
                ROBOT_POSITION_TOPIC, 
                ROBOT_PASSWORD,
                robotConnector,
                robotAdapter):
        super().__init__()
        self.running = True  # Flag de controle
        self.client =  client
        self.ROBOT_BRAND =  ROBOT_BRAND
        self.ROBOT_DESCRIPTION =  ROBOT_DESCRIPTION
        self.ROBOT_AXIS_NUMBER =  ROBOT_AXIS_NUMBER
        self.ROBOT_POSITION_TOPIC =  ROBOT_POSITION_TOPIC
        self.ROBOT_PASSWORD = ROBOT_PASSWORD
        self.robotConnector = robotConnector
        self.robotAdapter = robotAdapter
        
        self.newRobot = RobotDTO(ROBOT_BRAND, ROBOT_DESCRIPTION, ROBOT_AXIS_NUMBER)

    def run(self):
        print("Iniciando thread...", self)
        while self.running:  # Verifica a flag
            # print(self.running, self)
            self.sendRobotPosition()
    
    def stop(self):
        print("Parando a thread.", self)
        self.running = False  # Altera a flag para parar o loop
        
    def sendRobotPosition(self):
            # try:
                robot_information = RobotController.getRobotInfo(self.newRobot, self.robotConnector, self.robotAdapter)
                if self.client.is_connected():
                    # print("Estou conectado, publicando...", self.ROBOT_POSITION_TOPIC , robot_information)
                    self.client.publish(self.ROBOT_POSITION_TOPIC , robot_information)
            # except:
            #     pass

def createRobotThread(connection, robot, client):
    topic = connection.topic
    ip = connection.ip
    port = connection.port
    description = connection.description
    # number = connection.number
    password = connection.token
    if robot.type == "HC10":
        robotConnector = yaskawaHC10Connection(ip, port)
        robotAdapter = YaskawaRobotAdapter()
    if robot.type == "GP8":
        robotConnector = yaskawaGP8Connection(ip, port)
        robotAdapter = YaskawaRobotAdapter()
    if robot.type == "MIR100":
        robotConnector = MIRConnection(ip, password)
        robotAdapter = MirAdapter()
    robotThread = MinhaThread(client, robot.brand, description, robot.axis, topic, password, robotConnector, robotAdapter)
    # robotThread = threading.Thread(target=sendRobotPosition, args=(client, robot.brand, description, robot.axis, topic, password, robotConnector, robotAdapter))
    return robotThread

        

# createThreads()

# for key in threadList:
#     threadList[key].start()

# client.loop_start()