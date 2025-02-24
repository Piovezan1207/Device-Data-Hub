from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface
from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface

from src.web.pkg.DTO.RobotDTO import RobotDTO
from src.web.pkg.DTO.connectionDTO import ConnectionDTO

class dataBaseGateway(DataBaseGatewayInterface):
    def __init__(self,
                 dataBaseExternal: DataBaseExternalInterface):
        self._dataBaseExternal = dataBaseExternal
    
    def createConnection(self,
                         ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str, 
                        robotId: int) -> ConnectionDTO:
        
        conn = {
            "robot_id" : robotId,
            "ip": ip,
            "port": port,
            "description": description,
            "token": token,
            "topic": mqttTopic
        }
        
        id = self._dataBaseExternal.create(conn, "connections")
        
        connectionDto = ConnectionDTO(id, ip, port, description, token, mqttTopic)
        
        return connectionDto
        
        
        
    def getConnection(self, id) -> ConnectionDTO:
        conn = self._dataBaseExternal.get(id, "connections")
        
        connectionDto = ConnectionDTO(conn["id"], conn["ip"], conn["port"], conn["description"], conn["token"], conn["mqttTopic"])
        
        return connectionDto
    
    
    
    def getAllConnections(self) -> list[ConnectionDTO]:
        connections = self._dataBaseExternal.getAll("connections")
        
        return [ConnectionDTO(conn["id"], conn["ip"], conn["port"], conn["description"], conn["token"], conn["mqttTopic"]) for conn in connections]
     
    def updateConnection(self, id, connection) -> ConnectionDTO:
        conn = {
            "robot_id" : connection.robot.id,
            "ip": connection.ip,
            "port": connection.port,
            "description": connection.description
        }
        
        self._dataBaseExternal.update(id, conn, "connections")
        return ConnectionDTO(id, connection.ip, connection.port, connection.description, connection.token, connection.mqttTopic)
    
    def deleteConnection(self, id) -> bool:
        if self._dataBaseExternal.delete(id, "connections"):
            return True
        else:
            return False
    
    #################################################################################################################
    
    def createRobot(self,
                    typeR: str,
                    axis: int,
                    brand: str) -> RobotDTO:
        
        robot = {
            "type": typeR,
            "axis": axis,
            "brand": brand
        }
        
        id = self._dataBaseExternal.create(robot, "robots")
        
        RobotDTO = RobotDTO(id, typeR, axis, brand)
        
        return RobotDTO
    
    
    
    def getRobot(self, id) -> RobotDTO:
        robot = self._dataBaseExternal.get(id, "robots")
        
        RobotDto = RobotDTO(robot["id"], robot["type"], robot["axis"], robot["brand"])
        
        return RobotDto
    
    
    
    def getAllRobots(self) -> list[RobotDTO]:
        robots = self._dataBaseExternal.getAll("robots")
        
        return [RobotDTO(robot["id"], robot["type"], robot["axis"], robot["brand"]) for robot in robots]
    
 
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
        if self._dataBaseExternal.delete(id, "robots"):
            return True
        else:
            return False