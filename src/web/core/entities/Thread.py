from src.web.core.entities.Connection import Connection
from src.web.core.entities.MqttBroker import MqttBroker

class Thread:
    def __init__(self,
                 connection: Connection,
                 mqttBroker: MqttBroker,
                 id: int,
                 status: str):
        
        self._connection = connection
        self._mqttBroker = mqttBroker
        self._id = id
        self._status = status
        
    
    @property
    def connection(self) -> Connection:
        return self._connection
    
    @property
    def mqttBroker(self) -> MqttBroker:
        return self._mqttBroker
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, status: str):
        self._status = status