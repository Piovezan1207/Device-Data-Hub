from abc import ABC, abstractmethod
from src.robot.core.entities.robot import Robot

class RobotGatewayInterface:
    
    @abstractmethod
    def getRobotInformation() -> list:
        pass


