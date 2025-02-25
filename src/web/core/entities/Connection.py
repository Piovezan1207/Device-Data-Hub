from src.robot.core.entities.Robot import Robot
from src.web.core.entities.Sender import Sender
from src.web.core.entities.Status import Status

class Connection:
    def __init__(self, id: int,
                    ip: str,
                    port: int,
                    description: str,
                    token: str,
                    mqttTopic: str,
                    robot: Robot,
                    sender: Sender,
                    status: Status = None
                    ):

        self._id = id
        self._ip = ip
        self._port = port
        self._description = description
        self._token = token
        self._mqttTopic = mqttTopic
        self._robot = robot
        self._sender = sender
        if status is None:
            self._status = Status(False, False, False, "")
        else:
            self._status = status

    
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
    
    @property
    def status(self) -> Status:
        return self._status 
    
    @status.setter
    def status(self, status: Status):
        self._status = status

    