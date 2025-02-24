from abc import ABC, abstractmethod

from src.web.core.entities.Connection import Connection
from src.web.pkg.DTO.connectionDTO import ConnectionDTO

from src.web.pkg.DTO.RobotDTO import RobotDTO


class DataBaseGatewayInterface():
    
    @abstractmethod
    def createConnection(self,
                        ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str, 
                        robotId: int) -> Connection:
        pass
    
    @abstractmethod
    def getConnection(self, id) -> ConnectionDTO:
        pass
    
    @abstractmethod
    def getAllConnections(self) -> list[ConnectionDTO]:
        pass

    @abstractmethod 
    def updateConnection(self, id, connection) -> ConnectionDTO:
        pass
    
    @abstractmethod
    def deleteConnection(self, id) -> bool:
        pass

    ################################################################
    
    @abstractmethod
    def createRobot(self, 
                    typeR: str,
                    axis: int,
                    brand: str) -> RobotDTO:
        pass
    
    @abstractmethod
    def getRobot(self, id) -> RobotDTO:
        pass
    
    @abstractmethod
    def getAllRobots(self) -> list[RobotDTO]:
        pass
    
    @abstractmethod 
    def updateRobot(self, id, robot) -> RobotDTO:
        pass

    @abstractmethod
    def deleteRobot(self, id) -> bool:
        pass
    
    