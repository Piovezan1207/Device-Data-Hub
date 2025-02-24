from abc import ABC, abstractmethod


class ConnectionExternalInterface():
    
    @abstractmethod
    def createConnection(self, connection, mqttBroker) -> str:
        pass
    
    @abstractmethod
    def closeAllConnections(self) -> bool:
        pass
    
    @abstractmethod
    def closeConnection(self, id) -> bool:
        pass
    
    @abstractmethod
    def getConnectionData(self, id) -> str:
        pass

    
class DataBaseExternalInterface():
    
    @abstractmethod
    def get(self, id, table) -> str:
        pass
    
    @abstractmethod
    def getAll(self, table) -> str:
        pass
    
    @abstractmethod
    def create(self, data, table) -> str:
        pass
    
    @abstractmethod
    def update(self, id, data, table) -> str:
        pass
    
    @abstractmethod
    def delete(self, id, table) -> str:
        pass
    
    