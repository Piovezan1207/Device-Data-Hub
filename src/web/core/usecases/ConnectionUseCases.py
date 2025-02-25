from src.web.core.entities.Connection import Connection
from src.web.core.entities.Status import Status
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
                dataBaseGateway: DataBaseGatewayInterface,
                senderClient) -> Connection:
        
        
        robot= RobotUseCases.getRobot(robotId, dataBaseGateway)
        
        if robot is None:
            raise Exception("Robot not found")
        
        connectionDto = dataBaseGateway.createConnection(ip, port, description, token, mqttTopic, robotId)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=senderClient) #Adiciona objeto MQTT no sender!

        return connection
    
    
    
    @staticmethod
    def getConnection(id: int, dataBaseGateway: DataBaseGatewayInterface, senderClient, connectionExternal: ConnectionExternalInterface) -> Connection:
        connectionDto = dataBaseGateway.getConnection(id)
        
        if connectionDto is None:
            raise Exception("Connection not found")
        
        robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
        status = ConnectionUseCases.getConnectionStatus(connectionDto.id, connectionExternal)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=senderClient, status=status) #Adiciona objeto MQTT no sender!

        return connection
    
    @staticmethod   
    def getAllConnections(dataBaseGateway: DataBaseGatewayInterface, senderClient, connectionExternal: ConnectionExternalInterface) -> list[Connection]:
        
        connectionDtos =  dataBaseGateway.getAllConnections()
    
        connections = []
        
        for connectionDto in connectionDtos:
            robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
            status = ConnectionUseCases.getConnectionStatus(connectionDto.id, connectionExternal)
            connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, sender=senderClient, status=status) #Adiciona objeto MQTT no sender!
            connections.append(connection)
        
        return connections
    
    @staticmethod
    def runConnection(connection: Connection, connectionExternal: ConnectionExternalInterface) -> Connection:
        
        connection = connectionExternal.createConnection(connection)
        # connection.status = "connected"
        return connection
    
    
    @staticmethod
    def closeConnection(connection: Connection, connectionExternal: ConnectionExternalInterface) -> bool:
        
        # connection = ConnectionUseCases.getConnection(id, dataBaseGateway)
        status = connectionExternal.closeConnection(connection.id)
        status = ConnectionUseCases.getConnectionStatus(connection.id, connectionExternal)
        connection = ConnectionUseCases.DtoToEntitie(connection, robot=connection.robot, sender=connection.sender, status=status)
        
        return connection
    
    @staticmethod
    def deleteConnection(id: int, dataBaseGateway: DataBaseGatewayInterface, connectionExternal: ConnectionExternalInterface) -> bool:
        connection = ConnectionUseCases.closeConnection(id, dataBaseGateway, connectionExternal)
        
        delete =  dataBaseGateway.deleteConnection(id)
        
        if not delete:
            raise Exception("Connection not found")
        
        return connection
        
    
    @staticmethod
    def getConnectionStatus(id: int, connectionExternal: ConnectionExternalInterface) -> Status:
        
        statusObj =  connectionExternal.getConnectionStatus(id)
        
        status = Status(statusObj["running"], statusObj["connected"], statusObj["error"], statusObj["message"])
        
        return status
        
    
    @staticmethod
    def DtoToEntitie(connectionDto: ConnectionDTO, robot = None, sender = None, status = None) -> Connection:
        return Connection(connectionDto.id, 
                          connectionDto.ip, 
                          connectionDto.port, 
                          connectionDto.description, 
                          connectionDto.token, 
                          connectionDto.mqttTopic, 
                          robot, 
                          sender,
                          status)