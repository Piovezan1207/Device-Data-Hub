from src.robot.core.entities.robot import Robot
from src.web.core.entities.broker import Broker
from src.web.core.entities.status import Status

class Connection:
    def __init__(self, id: int,
                    ip: str,
                    port: int,
                    description: str,
                    token: str,
                    mqttTopic: str,
                    robot: Robot,
                    broker: Broker,
                    status: Status = None
                    ):

        self._id = id
        self._ip = ip
        self._port = port
        self._description = description
        self._token = token
        self._mqttTopic = mqttTopic
        self._robot = robot
        self._broker = broker
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
    def broker(self) -> Broker:
        return self._broker
    
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

    