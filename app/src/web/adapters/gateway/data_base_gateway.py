from app.src.web.pkg.interfaces.gateway_interfaces import DataBaseGatewayInterface
from app.src.web.pkg.interfaces.external_interfaces import DataBaseExternalInterface

from app.src.web.pkg.DTO.robot_dto import RobotDTO
from app.src.web.pkg.DTO.connection_dto import ConnectionDTO
from app.src.web.pkg.DTO.broker_dto import BrokerDTO


from dotenv import load_dotenv
import os

load_dotenv()

from cryptography.fernet import Fernet


f = Fernet(os.getenv("APP_KEY").encode())



class DataBaseGateway(DataBaseGatewayInterface):
    def __init__(self,
                 dataBaseExternal: DataBaseExternalInterface):
        self._dataBaseExternal = dataBaseExternal
    
    def createConnection(self,
                         ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str, 
                        robotId: int,
                        brokerId: int) -> ConnectionDTO:
        
        conn = {
            "robot_id" : robotId,
            "ip": ip,
            "port": port,
            "description": description,
            "token": token,
            "topic": mqttTopic,
            "broker_id": brokerId
        }
        
        id = self._dataBaseExternal.create(conn, "connections")
        
        connectionDto = ConnectionDTO(id=id, robotId=robotId, ip=ip, port=port, description=description, token=token, mqttTopic=mqttTopic, brokerId=brokerId)
        
        return connectionDto    
        
    def getConnection(self, id) -> ConnectionDTO:
        connections = self._dataBaseExternal.get(id, "connections")
        
        if connections is None:
            return None
            # raise Exception("Connection {} not found".format(id))
             
        connectionDto = ConnectionDTO(connections[0], connections[1], connections[2], connections[3], connections[4], connections[5], connections[6], connections[7])
        
        return connectionDto
    
    def getAllConnections(self) -> list[ConnectionDTO]:
        connections = self._dataBaseExternal.getAll("connections")
        if connections is None:
            return None
            # raise Exception("No connections found.")
        
        return [ConnectionDTO(connection[0], connection[1], connection[2], connection[3], connection[4], connection[5], connection[6], connection[7]) for connection in connections]
     
    def updateConnection(self, id, 
                         ip: str, 
                            port: int,
                            description: str, 
                            token: str, 
                            mqttTopic: str, 
                            robotId: int,
                            brokerId: int) -> ConnectionDTO:
        conn = {
            "robot_id" : robotId,
            "ip": ip,
            "port": port,
            "description": description,
            "token": token,
            "topic": mqttTopic,
            "broker_id": brokerId
        }
        
        self._dataBaseExternal.update(id, conn, "connections")
        return ConnectionDTO(id=id, robotId=robotId, brokerId=brokerId, mqttTopic=mqttTopic, ip=ip, port=port, description=description, token=token)
    
    def deleteConnection(self, id) -> bool:
        
        connection = self.getConnection(id)
        
        try:
            self._dataBaseExternal.delete(id, "connections")
            return connection
        except:
            raise Exception("Error deleting connection {}".format(id))
    
    #################################################################################################################
    
    def createRobot(self,
                    type: str,
                    axis: int,
                    brand: str) -> RobotDTO:
        
        robot = {
            "type": type,
            "axis": axis,
            "brand": brand
        }
        
        id = self._dataBaseExternal.create(robot, "robots")
        
        robotDTO = RobotDTO(id, type, axis, brand)
        
        return robotDTO
    
    def getRobot(self, id) -> RobotDTO:
        robot = self._dataBaseExternal.get(id, "robots")
        
        if robot is None:
            return None
        
        RobotDto = RobotDTO(robot[0], robot[1], robot[2], robot[3])
        
        return RobotDto
    
    def getAllRobots(self) -> list[RobotDTO]:
        robots = self._dataBaseExternal.getAll("robots")
        
        if robots is None:
            return None
            # raise Exception("No robots found.")
        
        return [RobotDTO(robot[0], robot[1], robot[2], robot[3]) for robot in robots]
    
    def updateRobot(self, id, robot) -> RobotDTO:
        robot = {
            "type": robot.type,
            "axis": robot.axis,
            "brand": robot.brand
        }
        
        self._dataBaseExternal.update(id, robot, "robots")
        
        RobotDTO = RobotDTO(id, robot.type, robot.axis, robot.brand)
        
        return RobotDTO

    def deleteRobot(self, id) -> bool:
        
        robot = self.getRobot(id)
        
        try:
            self._dataBaseExternal.delete(id, "robots")
            return robot
        except:
            raise Exception("Error deleting robot {}".format(id))
    
    #################################################################################################################
    
    def createBroker(self,
                    ip: str,
                    port: int,
                    user: str, 
                    password: str,
                    nickname: str) -> BrokerDTO:
        
        broker = {
            "ip": ip,
            "port": port,
            "user": user,
            "password": f.encrypt(password.encode()),
            "nickname" : nickname
        }
        
        id = self._dataBaseExternal.create(broker, "brokers")
        
        brokerDTO = BrokerDTO(id, ip, port, user, password, nickname)
        
        return brokerDTO
    
    def getBroker(self, id) -> BrokerDTO:
        broker = self._dataBaseExternal.get(id, "brokers")
        
        if broker is None:
            return None
        
        
        brokerDTO = BrokerDTO(broker[0], broker[1], broker[2], broker[3], f.decrypt(broker[4]).decode(), broker[5])
        
        return brokerDTO
    
    def getAllBrokers(self) -> list[BrokerDTO]:
        brokers = self._dataBaseExternal.getAll("brokers", withDeleted=False)
        
        if brokers is None:
            return None

        return [BrokerDTO(broker[0], broker[1], broker[2], broker[3], f.decrypt(broker[4]).decode(), broker[5]) for broker in brokers]
    
    def updateBroker(self, id, broker) -> BrokerDTO:
        broker = {
            "ip": broker.ip,
            "port": broker.port,
            "user": broker.user,
            "password": f.encrypt(broker.password.encode()),
            "nickname": broker.nickname
        }
        
        self._dataBaseExternal.update(id, broker, "brokers")
        
        brokerDTO = BrokerDTO(id, broker.ip, broker.port, broker.user, broker.password, broker.nickname)
        
        return brokerDTO

    def deleteBroker(self, id) -> bool:
        
        broker = self.getBroker(id)
        
        # try:
        self._dataBaseExternal.softDelete(id, "brokers")
        return broker
        # except:
        #     raise Exception("Error deleting robot {}".format(id))
    