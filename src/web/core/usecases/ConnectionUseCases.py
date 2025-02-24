from src.web.core.entities.Connection import Connection
from src.web.pkg.DTO.connectionDTO  import ConnectionDTO

from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface
from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface

from src.web.core.usecases.RobotUseCases import RobotUseCases

class ConnectionUseCases:
    
    @staticmethod
    def create(
                ip: str, 
                port: int,
                description: str, 
                token: str, 
                mqttTopic: str, 
                robotId: int, 
                connectionExternal : ConnectionExternalInterface,
                dataBaseGateway: DataBaseGatewayInterface) -> Connection:
        
        
        robot= RobotUseCases.getRobot(robotId, dataBaseGateway)
        
        if robot is None:
            raise Exception("Robot not found")
        
        connectionDto = dataBaseGateway.createConnection(ip, port, description, token, mqttTopic, robotId)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=None) #Adiciona objeto MQTT no sender!

        connection = connectionExternal.createConnection(connection)
        return connection
    
    
    
    @staticmethod
    def getConnection(id: int, dataBaseGateway: DataBaseGatewayInterface) -> Connection:
        connectionDto = dataBaseGateway.getConnection(id)
        
        if connectionDto is None:
            raise Exception("Connection not found")
        
        robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=None) #Adiciona objeto MQTT no sender!
        
        return connection
    
    @staticmethod   
    def getAllConnections(dataBaseGateway: DataBaseGatewayInterface) -> list[Connection]:
        
        connectionDtos =  dataBaseGateway.getAllConnections()
    
        connections = []
        
        for connectionDto in connectionDtos:
            robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
            connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=None) #Adiciona objeto MQTT no sender!
            connections.append(connection)
        
        return connections
    
    @staticmethod
    def runConnection(id: int, connectionExternal: ConnectionExternalInterface, 
                      dataBaseGateway: DataBaseGatewayInterface) -> Connection:
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway)
        connection = connectionExternal.createConnection(connection)
        
        return connection
    
    @staticmethod
    def runAllConnections(connectionExternal: ConnectionExternalInterface, 
                          dataBaseGateway: DataBaseGatewayInterface) -> list[Connection]:
        
        connections = ConnectionUseCases.getAllConnections(dataBaseGateway)
        
        for connection in connections:
            connection = connectionExternal.createConnection(connection)
        
        return connections
    
    @staticmethod
    def closeConnection(id: int, connectionExternal: ConnectionExternalInterface, 
                        dataBaseGateway: DataBaseGatewayInterface) -> bool:
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway)
        connection = connectionExternal.closeConnection(connection)
        
        return connection
    
    @staticmethod
    def DtoToEntitie(connectionDto: ConnectionDTO, robot = None, sender = None) -> Connection:
        return Connection(connectionDto.id, 
                          connectionDto.ip, 
                          connectionDto.port, 
                          connectionDto.description, 
                          connectionDto.token, 
                          connectionDto.mqttTopic, 
                          robot, 
                          sender)