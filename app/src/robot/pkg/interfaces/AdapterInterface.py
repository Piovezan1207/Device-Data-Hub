from abc import ABC, abstractmethod
from src.robot.core.entities.Robot import Robot
from src.robot.core.entities.Request import Request

class RobotAdapterInterface():
    @abstractmethod
    def adaptRobotInformationsToDT(robot: Robot):
        pass


class RequestAdapterInterface():
    @abstractmethod
    def adaptRequestInformations(request: Request):
        pass