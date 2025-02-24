from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface
from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface

from src.web.pkg.DTO.RobotDTO import RobotDTO
from src.web.pkg.DTO.connectionDTO import ConnectionDTO

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
        
        connectionDto = ConnectionDTO(id, robotId, ip, port, description, token, mqttTopic)
        
        return connectionDto
        
        
        
    def getConnection(self, id) -> ConnectionDTO:
        connections = self._dataBaseExternal.get(id, "connections")
        
        if connections is None:
            raise Exception("Connection {} not found".format(id))
             
        connectionDto = ConnectionDTO(connections[0], connections[1], connections[2], connections[3], connections[4], connections[5], connections[6])
        
        return connectionDto
    
    
    
    def getAllConnections(self) -> list[ConnectionDTO]:
        connections = self._dataBaseExternal.getAll("connections")
        
        if connections is None:
            raise Exception("No connections found.")
        
        return [ConnectionDTO(connection[0], connection[1], connection[2], connection[3], connection[4], connection[5], connection[6]) for connection in connections]
     
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
        
        print(id)
        
        robotDTO = RobotDTO(id, type, axis, brand)
        
        return robotDTO
    
    
    
    def getRobot(self, id) -> RobotDTO:
        robot = self._dataBaseExternal.get(id, "robots")
        
        if robot is None:
            raise Exception("Robot {} not found".format(id))
        
        RobotDto = RobotDTO(robot[0], robot[1], robot[2], robot[3])
        
        return RobotDto
    
    
    
    def getAllRobots(self) -> list[RobotDTO]:
        robots = self._dataBaseExternal.getAll("robots")
        
        if robots is None:
            raise Exception("No robots found.")
        
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