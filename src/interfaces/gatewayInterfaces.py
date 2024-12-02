from abc import ABC, abstractmethod
from ..entities.Robot import Robot

class RobotGatewayInterface:
    
    @abstractmethod
    def getRobotInformation() -> list:
        pass


