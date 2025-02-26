from src.web.core.entities.Sender import Sender
from src.web.core.entities.Connection import Connection
from src.web.core.entities.Robot import Robot

from src.web.pkg.DTO.RobotDTO import RobotDTO

from src.web.pkg.interfaces.externalInterfaces import ConnectionExternalInterface
from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface

class RobotUseCases:
    
    @staticmethod
    def create(typeR: str,
                axis: int,
                brand: str, 
                dataBaseGateway: DataBaseGatewayInterface) -> Robot:
        
        robotDto = dataBaseGateway.createRobot(typeR, brand, axis)
        
        robot = RobotUseCases.DtoToEntitie(robotDto)
        
        return robot
    
    @staticmethod
    def getRobot(id: int, dataBaseGateway: DataBaseGatewayInterface) -> Robot:
        robotDto = dataBaseGateway.getRobot(id)
        
        if robotDto is None:
            return None
            # raise Exception("Robot not found")
        
        robot = RobotUseCases.DtoToEntitie(robotDto)
        
        return robot
    
    @staticmethod
    def getAllRobots(dataBaseGateway: DataBaseGatewayInterface) -> list[Robot]:
        robotDtos = dataBaseGateway.getAllRobots()
        
        if robotDtos is None:
            return None
        
        robots = []
        
        for robotDto in robotDtos:
            robot = RobotUseCases.DtoToEntitie(robotDto)
            robots.append(robot)
            
        return robots
    
    @staticmethod
    def deleteRobot(id: int, dataBaseGateway: DataBaseGatewayInterface) -> bool:
        return dataBaseGateway.deleteRobot(id)
    
    @staticmethod
    def DtoToEntitie(robotDto: RobotDTO) -> Robot:
        return Robot(robotDto.id, robotDto.type, robotDto.axis, robotDto.brand)