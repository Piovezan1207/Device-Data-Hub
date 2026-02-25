
from src.web.core.entities.connection import Connection

from app.src.web.core.usecases.connection_use_cases import ConnectionUseCases

from app.src.web.adapters.gateway.data_base_gateway import DataBaseGateway

from app.src.web.pkg.interfaces.gateway_interfaces import DataBaseGatewayInterface
from app.src.web.pkg.interfaces.external_interfaces import ConnectionExternalInterface, DataBaseExternalInterface

from app.src.web.pkg.interfaces.adapter_interfaces import ConnectAdapterInterface
from app.src.web.adapters.presenter.connection_presenter import DefaultConnectionPresenter



# from src.web.adapters.controller.RobotController import RobotController

class ConnectionController:
    
    @staticmethod
    def runAllConnections(dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connections  = ConnectionUseCases.getAllConnections(dataBaseGateway, connectionExternal)
        # print(connections)
        if connections:
            connectionsList = []
            
            for conn in connections:
                newConn = ConnectionUseCases.runConnection(conn, connectionExternal)
                connectionsList.append(newConn)
                
            connections = connectionsList
        
        adapter =  connectAdapter()
        return adapter.adaptConnectionsInformation(connections)
    
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
                brokerId: int,
                dataBaseExternal: DataBaseExternalInterface,
                connectionExternal: ConnectionExternalInterface,
                connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter,
                runConnection = True):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.create(ip, port, description, token, mqttTopic, robotId, brokerId, dataBaseGateway)
        
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
        connection = ConnectionUseCases.closeConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)
    
    @staticmethod 
    def updateConnection(id: int, ip: str, port: int, description: str, token: str, mqttTopic: str, robotId: int, brokerId:int, dataBaseExternal: DataBaseExternalInterface, connectionExternal: ConnectionExternalInterface, connectAdapter: ConnectAdapterInterface = DefaultConnectionPresenter, runConnection = True):
        
        dataBaseGateway = DataBaseGateway(dataBaseExternal)
        
        connection = ConnectionUseCases.getConnection(id, dataBaseGateway, connectionExternal)
        
        if connection:

            connection = ConnectionUseCases.closeConnection(connection, connectionExternal)
            connection = ConnectionUseCases.updateConnection(id, ip, port, description, token, mqttTopic, robotId, brokerId, dataBaseGateway)
            if runConnection:
                connection = ConnectionUseCases.runConnection(connection, connectionExternal)
        
        adapter =  connectAdapter()
        
        return adapter.adaptConnectionInformation(connection)