from abc import ABC, abstractmethod


from app.src.web.pkg.DTO.connection_dto import ConnectionDTO

from app.src.web.pkg.DTO.robot_dto import RobotDTO

from app.src.web.pkg.DTO.broker_dto import BrokerDTO


class DataBaseGatewayInterface():
    
    @abstractmethod
    def createConnection(self,
                        ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str,
                        brokerId: int, 
                        robotId: int) -> ConnectionDTO:
        pass
    
    @abstractmethod
    def getConnection(self, id) -> ConnectionDTO:
        pass
    
    @abstractmethod
    def getAllConnections(self) -> list[ConnectionDTO]:
        pass

    @abstractmethod 
    def updateConnection(self, 
                         id:int, 
                        ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str, 
                        brokerId: int,
                        robotId: int) -> ConnectionDTO:
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
   
   ################################################################
   
    @abstractmethod
    def createBroker(self, 
                    ip: str,
                    port: int,
                    user: str, 
                    password: str,
                    nickname: str) -> BrokerDTO:
        pass
    
    @abstractmethod
    def getBroker(self, id) -> BrokerDTO:
        pass
    
    @abstractmethod
    def getAllBrokers(self) -> list[BrokerDTO]:
        pass
    
    @abstractmethod 
    def updateBroker(self, id, Broker) -> BrokerDTO:
        pass

    @abstractmethod
    def deleteBroker(self, id) -> bool:
        pass
    
    