
from src.web.core.entities.Connection import Connection

from src.web.core.usecases.ConnectionUseCases import ConnectionUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway

from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface
from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface, DataBaseExternalInterface

from src.web.pkg.interfaces.AdapterInterfaces import ConnectAdapterInterface
from src.web.adapters.presenter.ConnectionPresenter import DefaultConnectionPresenter

class ConnectionController:
    
    @staticmethod
    def runAllConnections(dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, senderClient, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections  = ConnectionUseCases.getAllConnections(dataBaseGateway, senderClient)

        newConnections = []
        
        for conn in connections:
            newConn = ConnectionUseCases.runConnection(conn, connectionExternal)
            newConnections.append(newConn)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionsInformation(newConnections)
    
    @staticmethod
    def deleteConnection(id: int, dataBaseExternal: DataBaseExternalInterface,  connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        deleted = ConnectionUseCases.deleteConnection(id, dataBaseGateway, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(deleted)
    
    @staticmethod
    def createConnection(ip: str, 
                port: int,
                description: str, 
                token: str, 
                mqttTopic: str, 
                robotId: int,
                dataBaseExternal: DataBaseExternalInterface,
                connectionExternal: ConnectionExternalInterface,
                senderClient,
                connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.create(ip, port, description, token, mqttTopic, robotId, dataBaseGateway, senderClient)
        
        newConnection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(newConnection)
    
    @staticmethod
    def getConnection(id: int, dataBaseExternal: DataBaseExternalInterface, senderClient, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, senderClient)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod
    def getAllConnections(dataBaseExternal: DataBaseExternalInterface, senderClient, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections = ConnectionUseCases.getAllConnections(dataBaseGateway, senderClient)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionsInformation(connections)