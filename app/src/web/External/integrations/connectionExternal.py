#################################################
"""
Implementa a arquitetura de coleta de dados dos rbôs.
"""
#################################################

from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface

from src.robot.pkg.DTO.RobotDTO import RobotDTO

from src.robot.adapters.controller.RobotController import RobotController

from src.robot.External.integrations.yaskawaHC10Connection import yaskawaHC10Connection
from src.robot.External.integrations.yaskawaGP8Connection import yaskawaGP8Connection
from src.robot.adapters.presenter.YaskawaRobotAdapter import YaskawaRobotAdapter

from src.robot.External.integrations.MIRConnection import MIRConnection
from src.robot.adapters.presenter.MirAdapter import MirAdapter

from src.robot.adapters.controller.RobotController import RobotController

import threading

#################################################
import paho.mqtt.client as mqtt

from dotenv import load_dotenv
import os

load_dotenv()



#################################################

class ThreadManager:
    def __init__(self):
        self._threadList = {}
    
    @property
    def threadList(self) -> dict:
        return self._threadList
    
    def addThread(self, thread, id):
        self._threadList[id] = thread
        thread.start()
        return True
    
    def runThread(self, id):
        self._threadList[id].start()
        return True
    
    def stopThread(self, id):
        if id in self._threadList:
            self._threadList[id].stop()
            self._threadList[id].join()
            self._threadList.pop(id)
            return True
        
    
    def stopAllThreads(self):
        for thread in self._threadList:
            thread.stop()
        self._threadList = {}
        return True
        
    def getThread(self, id):
        return self._threadList[id]
    
    def getStatus(self, id):
        if id in self._threadList:
            status = {
                "running": self._threadList[id]._runningStatus,
                "connected": self._threadList[id]._connectedStatus,
                "error": self._threadList[id]._errorStatus,
                "message": self._threadList[id]._messageStatus
            }
            
            return status
        
        else:
             status = {
                "running": False,
                "connected": False,
                "error": False,
                "message": "Thread not running."
            }

        return status



        
class getDataThread(threading.Thread):
    def __init__(self, 
                BROKER_INFO, 
                ROBOT_BRAND, 
                ROBOT_DESCRIPTION, 
                ROBOT_AXIS_NUMBER, 
                ROBOT_POSITION_TOPIC, 
                ROBOT_PASSWORD,
                robotConnector,
                robotAdapter,
                DEBUG=False):
        super().__init__()
        self.running = True  # Flag de controle
        # self.client =  client
        self.ROBOT_BRAND =  ROBOT_BRAND
        self.ROBOT_DESCRIPTION =  ROBOT_DESCRIPTION
        self.ROBOT_AXIS_NUMBER =  ROBOT_AXIS_NUMBER
        self.ROBOT_POSITION_TOPIC =  ROBOT_POSITION_TOPIC
        self.ROBOT_PASSWORD = ROBOT_PASSWORD
        self.robotConnector = robotConnector
        self.robotAdapter = robotAdapter
        
        self.newRobot = RobotDTO(ROBOT_BRAND, ROBOT_DESCRIPTION, ROBOT_AXIS_NUMBER)
        
        self._runningStatus = False
        self._connectedStatus = False
        self._errorStatus = False
        self._messageStatus = "Thread criada."
        
        
        self.BROKER = BROKER_INFO[0]
        self.PORT =  BROKER_INFO[1]
        self.client = mqtt.Client()
        self.client.username_pw_set(BROKER_INFO[2], BROKER_INFO[3])
        
        self._DEBUG = DEBUG

    def run(self):
        print("Iniciando thread...", self)
        self._runningStatus = True
        self._messageStatus = "Rodando!"
        while self.running:  # Verifica a flag
            
            if not self.client.is_connected():
                try:
                    self.client.connect(self.BROKER, self.PORT, 60)
                except Exception as e:
                    self._errorStatus = True
                    self._messageStatus = "Erro ao conectar com o broker."
                    if self._DEBUG:
                        self._messageStatus += "  {}".format(str(e))

                    self._runningStatus = True
                    self._connectedStatus = False
                    continue
            
            data = self.sendRobotPosition()
            if not data:
                continue
            
            try:
                self.client.publish(self.ROBOT_POSITION_TOPIC , data)
                self._connectedStatus = True
                self._messageStatus = "Rodando!"
                self._errorStatus = False
            except Exception as e:
                self._messageStatus = "Erro ao publicar no broker."
                if self._DEBUG:
                        self._messageStatus += "  {}".format(str(e))
                self._errorStatus = True
                self._runningStatus = True
                self._connectedStatus = False
                continue
        
        self._runningStatus = False
    
    def stop(self):
        print("Parando a thread.", self)
        self.running = False  # Altera a flag para parar o loop     
        self._runningStatus = False  
        
        if self.client.is_connected():
            self.client.disconnect()
    
    def sendRobotPosition(self):
        # robot_information = RobotController.getRobotInfo(self.newRobot, self.robotConnector, self.robotAdapter)
        # return robot_information
        try:
            robot_information = RobotController.getRobotInfo(self.newRobot, self.robotConnector, self.robotAdapter)
            return robot_information
        except Exception as e:
            self._connectedStatus = False
            self._errorStatus = True
            # self._messageStatus = "Problema ao se comunicar com o robô." #+ str(e)
            self._messageStatus = "Erro na comunicação com robô."
            if self._DEBUG:
                        self._messageStatus += "  {}".format(str(e))


class connectionExternal(ConnectionExternalInterface):
    def __init__(self, managerClass):
        self._manager = managerClass
        pass
    
    def createConnection(self, connection) :
        topic = connection.mqttTopic
        ip = connection.ip
        robot = connection.robot
        port = connection.port
        description = connection.description
        
        brokerIp = connection.broker.ip
        brokerPort = connection.broker.port
        brokerUser = connection.broker.user
        brokerPassword = connection.broker.password
        
        password = connection.token
        if robot.type == "HC10":
            robotConnector = yaskawaHC10Connection(ip, port)
            robotAdapter = YaskawaRobotAdapter()
        elif robot.type == "GP8":
            robotConnector = yaskawaGP8Connection(ip, port)
            robotAdapter = YaskawaRobotAdapter()
        elif robot.type == "MIR100":
            robotConnector = MIRConnection(ip, password)
            robotAdapter = MirAdapter()
        else:
            raise Exception("Robot not found")
        
        # BROKER_INFO = [BROKER_IP, BROKER_PORT, BROKER_USER, BROKER_PASSWORD]
        BROKER_INFO = [brokerIp, brokerPort, brokerUser, brokerPassword]
        
        # robotThread = getDataThread(mqttSender, robot.brand, description, robot.axis, topic, password, robotConnector, robotAdapter)
        robotThread = getDataThread(BROKER_INFO, robot.brand, description, robot.axis, topic, password, robotConnector, robotAdapter, DEBUG=os.getenv("DEBUG"))
        self._manager.addThread(robotThread, connection.id)

        # connection.status = "running"
            
        return connection
    
    def closeAllConnections(self):
        self._manager.stopAllThreads()
        self._manager.threadList = {}
        return True
    
    def closeConnection(self, id):
        self._manager.stopThread(id)
        # status = self._manager.getStatus(id)
        return True
    
    def getConnectionStatus(self, id):
        status = self._manager.getStatus(id)
        return status
