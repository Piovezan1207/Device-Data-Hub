from abc import ABC, abstractmethod

from src.web.core.entities.Connection import Connection
from src.web.core.entities.Robot import Robot
from src.web.core.entities.Broker import Broker

class RobotAdapterInterface():
    @abstractmethod
    def adaptRobotInformation(robot: Robot):
        pass
    
    @abstractmethod
    def adaptRobotsInformation(robot: Robot):
        pass

class ConnectAdapterInterface():
    @abstractmethod 
    def adaptConnectionInformation(connection: Connection):
        pass

    @abstractmethod 
    def adaptConnectionsInformation(connection: Connection):
        pass

class BrokerAdapterInterface():
    @abstractmethod 
    def adaptConnectionInformation(broker: Broker):
        pass

    @abstractmethod 
    def adaptConnectionsInformation(broker: Broker):
        pass
    

    