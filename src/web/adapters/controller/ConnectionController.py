
from src.web.core.entities.Connection import Connection

from src.web.core.usecases.ConnectionUseCases import ConnectionUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway

from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface
from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface, DataBaseExternalInterface


class ConnectionController:
    
    @staticmethod
    def runAllConnections(dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, senderClient):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections  = ConnectionUseCases.getAllConnections(dataBaseGateway, senderClient)

        newConnections = []
        
        for conn in connections:
            newConn = ConnectionUseCases.runConnection(conn, connectionExternal)
            newConnections.append(newConn)
            
        
        return newConnections #Adicionar adapter!!
    
    @staticmethod
    def deleteConnection(id: int, dataBaseExternal: DataBaseExternalInterface,  connectionExternal: ConnectionExternalInterface):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        deleted = ConnectionUseCases.deleteConnection(id, dataBaseGateway, connectionExternal)
        
        return deleted #Adicionar adapter!!
    
    @staticmethod
    def createConnection(ip: str, 
                port: int,
                description: str, 
                token: str, 
                mqttTopic: str, 
                robotId: int,
                dataBaseExternal: DataBaseExternalInterface,
                connectionExternal: ConnectionExternalInterface,
                senderClient):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.create(ip, port, description, token, mqttTopic, robotId, dataBaseGateway, senderClient)
        
        newConnection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        return newConnection #Adicionar adapter!!
    
    @staticmethod
    def getConnection(id: int, dataBaseExternal: DataBaseExternalInterface, senderClient):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, senderClient)
        
        return connection #Adicionar adapter!!
    
    @staticmethod
    def getAllConnections(dataBaseExternal: DataBaseExternalInterface, senderClient):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections = ConnectionUseCases.getAllConnections(dataBaseGateway, senderClient)
        
        return connections #Adicionar adapter!!