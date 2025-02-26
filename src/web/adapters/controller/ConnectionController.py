
from src.web.core.entities.Connection import Connection

from src.web.core.usecases.ConnectionUseCases import ConnectionUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway

from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface
from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface, DataBaseExternalInterface

from src.web.pkg.interfaces.AdapterInterfaces import ConnectAdapterInterface
from src.web.adapters.presenter.ConnectionPresenter import DefaultConnectionPresenter



# from src.web.adapters.controller.RobotController import RobotController

class ConnectionController:
    
    @staticmethod
    def runAllConnections(dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections  = ConnectionUseCases.getAllConnections(dataBaseGateway, connectionExternal)

        newConnections = []
        
        for conn in connections:
            newConn = ConnectionUseCases.runConnection(conn, connectionExternal)
            newConnections.append(newConn)
        
        adapter =  connectAdapter()
        return adapter.adaptConnectionsInformation(newConnections)
    
    @staticmethod
    def deleteConnection(id: int, dataBaseExternal: DataBaseExternalInterface,  connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        
        # return connection
        
        if connection:

            connection = ConnectionUseCases.deleteConnection(connection, dataBaseGateway, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod
    def createConnection(ip: str, 
                port: int,
                description: str, 
                token: str, 
                mqttTopic: str, 
                robotId: int,
                dataBaseExternal: DataBaseExternalInterface,
                connectionExternal: ConnectionExternalInterface,
                connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter,
                runConnection = True):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.create(ip, port, description, token, mqttTopic, robotId, dataBaseGateway)
        
        if runConnection:
            connection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod
    def getConnection(id: int, dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod
    def getAllConnections(dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections = ConnectionUseCases.getAllConnections(dataBaseGateway, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionsInformation(connections)
    

    @staticmethod
    def runConnection(id: int, dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        
        connection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod
    def stopConnection(id: int, dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        print("ue" , connection, "Ue")
        connection = ConnectionUseCases.closeConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod 
    def updateConnection(id: int, ip: str, port: int, description: str, token: str, mqttTopic: str, robotId: int, dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter, runConnection = True):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        
        if connection:

            connection = ConnectionUseCases.closeConnection(connection, connectionExternal)
            connection = ConnectionUseCases.updateConnection(id, ip, port, description, token, mqttTopic, robotId, dataBaseGateway)
            if runConnection:
                connection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)