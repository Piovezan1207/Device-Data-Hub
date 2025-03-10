from abc import ABC, abstractmethod

class RobotExternalInterface():
    
    @abstractmethod
    def getRobotPosition() -> list:
        pass
    
    @abstractmethod
    def getClawStatus() -> int:
        pass
    
    @abstractmethod
    def getRobotData() -> object:
        pass