from src.web.core.entities.broker import Broker
from src.web.core.entities.connection import Connection
from src.web.core.entities.robot import Robot

from app.src.web.pkg.DTO.robot_dto import RobotDTO

from app.src.web.pkg.interfaces.external_interfaces import ConnectionExternalInterface
from app.src.web.pkg.interfaces.gateway_interfaces import DataBaseGatewayInterface

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