from src.robot.core.entities.Robot import Robot
from web.core.entities.Sender import Sender

class Connection:
    def __init__(self, id: int,
                    ip: str,
                    port: int,
                    description: str,
                    token: str,
                    mqttTopic: str,
                    robot: Robot,
                    sender: Sender
                    ):

        self._id = id
        self._ip = ip
        self._port = port
        self._description = description
        self._token = token
        self._mqttTopic = mqttTopic
        self._robot = robot
        self._sender = sender
        self._status = "disconnected"
        
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def ip(self) -> str:
        return self._ip
    
    @property
    def port(self) -> int:
        return self._port
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def token(self) -> str:
        return self._token
    
    @property
    def mqttTopic(self) -> str:
        return self._mqttTopic
    
    @property
    def robot(self) -> Robot:
        return self._robot
    
    @property
    def sender(self) -> Sender:
        return self._sender
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, status: str):
        self._status = status
    

    