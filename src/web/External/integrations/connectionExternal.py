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
        print(id)
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
        
        self._runningStatus = False
        self._connectedStatus = False
        self._errorStatus = False
        self._messageStatus = "Thread created."

    def run(self):
        print("Iniciando thread...", self)
        self._runningStatus = True
        self._messageStatus = "Running!"
        while self.running:  # Verifica a flag
            # print(self.running, self)
            self.sendRobotPosition()
        
        self._runningStatus = False
    
    def stop(self):
        print("Parando a thread.", self)
        self.running = False  # Altera a flag para parar o loop     
        self._runningStatus = False  
    
    def sendRobotPosition(self):
        try:
            robot_information = RobotController.getRobotInfo(self.newRobot, self.robotConnector, self.robotAdapter)
            if robot_information:
                self._connectedStatus = True
            
            if self.client.is_connected():
                # print("Estou conectado, publicando...", self.ROBOT_POSITION_TOPIC , robot_information)
                self.client.publish(self.ROBOT_POSITION_TOPIC , robot_information)
            else:
                self._errorStatus = True
                self._messageStatus = str("Sender não conectado.")
            self._errorStatus = False
        except Exception as e:
            # print(e)
            self._connectedStatus = False
            self._errorStatus = True
            self._messageStatus = str(e)


class connectionExternal(ConnectionExternalInterface):
    def __init__(self, managerClass):
        self._manager = managerClass
        pass
    
    def createConnection(self, connection) :
        
        print(connection)
        
        topic = connection.mqttTopic
        ip = connection.ip
        robot = connection.robot
        port = connection.port
        description = connection.description
        mqttSender = connection.sender
        
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
        
        robotThread = getDataThread(mqttSender, robot.brand, description, robot.axis, topic, password, robotConnector, robotAdapter)
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
