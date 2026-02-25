from abc import ABC, abstractmethod
from src.robot.core.entities.robot import Robot
from src.robot.core.entities.request import Request

class RobotAdapterInterface():
    @abstractmethod
    def adaptRobotInformationsToDT(robot: Robot):
        pass


class RequestAdapterInterface():
    @abstractmethod
    def adaptRequestInformations(request: Request):
        pass