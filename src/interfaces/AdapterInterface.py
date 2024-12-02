from abc import ABC, abstractmethod
from ..entities.Robot import Robot
from ..entities.Request import Request

class RobotAdapterInterface():
    
    @abstractmethod
    def adaptRobotInformationsToDT(robot: Robot):
        pass


class RequestAdapterInterface():
    
    @abstractmethod
    def adaptRequestInformations(request: Request):
        pass