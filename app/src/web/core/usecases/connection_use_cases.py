from src.web.core.entities.connection import Connection
from src.web.core.entities.status import Status
from app.src.web.pkg.DTO.connection_dto  import ConnectionDTO

from app.src.web.pkg.interfaces.external_interfaces import ConnectionExternalInterface
from app.src.web.pkg.interfaces.gateway_interfaces import DataBaseGatewayInterface

from app.src.web.core.usecases.robot_use_cases import RobotUseCases
from app.src.web.core.usecases.broker_use_cases import BrokerUseCases

class ConnectionUseCases:
    
    @staticmethod
    def create(
                ip: str, 
                port: int,
                description: str, 
                token: str, 
                mqttTopic: str, 
                robotId: int, 
                brokerId: int,
                dataBaseGateway: DataBaseGatewayInterface
                ) -> Connection:
        
        
        robot= RobotUseCases.getRobot(robotId, dataBaseGateway)
        
        if robot is None:
            raise Exception("Robot not found")
        
        broker = BrokerUseCases.getBroker(brokerId, dataBaseGateway)
        
        if broker is None:
            raise Exception("Broker not found")
        
        connectionDto = dataBaseGateway.createConnection(ip, port, description, token, mqttTopic, robotId, brokerId)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, broker=broker ) 

        return connection
    
    
    
    @staticmethod
    def getConnection(id: int, dataBaseGateway: DataBaseGatewayInterface, connectionExternal: ConnectionExternalInterface) -> Connection:
        connectionDto = dataBaseGateway.getConnection(id)
        
        if connectionDto is None:
           return None
        
        robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
        broker = BrokerUseCases.getBroker(connectionDto.brokerId, dataBaseGateway)
        status = ConnectionUseCases.getConnectionStatus(connectionDto.id, connectionExternal)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot,  status=status, broker=broker) 

        return connection
    
    @staticmethod   
    def getAllConnections(dataBaseGateway: DataBaseGatewayInterface, connectionExternal: ConnectionExternalInterface) -> list[Connection]:
        
        connectionDtos =  dataBaseGateway.getAllConnections()

        if connectionDtos is None:
           return None
        
        connections = []
        
        for connectionDto in connectionDtos:
            robot = RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
            broker = BrokerUseCases.getBroker(connectionDto.brokerId, dataBaseGateway)
            status = ConnectionUseCases.getConnectionStatus(connectionDto.id, connectionExternal)
            connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot,  status=status, broker=broker) 
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
        connection = ConnectionUseCases.DtoToEntitie(connection, robot=connection.robot,status=status, broker=connection.broker)
        
        return connection
    
    @staticmethod
    def deleteConnection(connection: Connection,  dataBaseGateway: DataBaseGatewayInterface, connectionExternal: ConnectionExternalInterface) -> bool:
        
        connection = ConnectionUseCases.closeConnection(connection, connectionExternal)
        
        delete =  dataBaseGateway.deleteConnection(connection.id)
        
        if not delete:
            raise Exception("Connection not found")
        
        return connection
        
    
    @staticmethod
    def getConnectionStatus(id: int, connectionExternal: ConnectionExternalInterface) -> Status:
        
        statusObj =  connectionExternal.getConnectionStatus(id)
        
        status = Status(statusObj["running"], statusObj["connected"], statusObj["error"], statusObj["message"])
        
        return status
        
    @staticmethod
    def updateConnection(id: int,
                        ip: str, 
                        port: int,
                        description: str, 
                        token: str, 
                        mqttTopic: str, 
                        robotId: int, 
                        brokerId: int,
                        dataBaseGateway: DataBaseGatewayInterface,
                        ) -> Connection:
        
        connectionDto = dataBaseGateway.updateConnection(id, ip, port, description, token, mqttTopic, robotId, brokerId)
        
        robot= RobotUseCases.getRobot(connectionDto.robotId, dataBaseGateway)
        
        broker = BrokerUseCases.getBroker(connectionDto.brokerId, dataBaseGateway)
        
        connection = ConnectionUseCases.DtoToEntitie(connectionDto, robot=robot, broker=broker)
        
        return connection
    
    @staticmethod
    def DtoToEntitie(connectionDto: ConnectionDTO, robot = None,  status = None, broker=None) -> Connection:
        return Connection(id=connectionDto.id, 
                          ip=connectionDto.ip, 
                          port=connectionDto.port, 
                          description=connectionDto.description, 
                          token=connectionDto.token, 
                          mqttTopic=connectionDto.mqttTopic, 
                          robot=robot, 
                          broker=broker,
                          status=status)