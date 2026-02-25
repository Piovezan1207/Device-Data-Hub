from abc import ABC, abstractmethod

from src.web.core.entities.connection import Connection
from src.web.core.entities.robot import Robot
from src.web.core.entities.broker import Broker

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
    def adaptBrokerInformation(broker: Broker):
        pass

    @abstractmethod 
    def adaptBrokersInformation(broker: Broker):
        pass
    

    