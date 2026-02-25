from src.robot.core.entities.robot import Robot
from src.robot.core.entities.request import Request
from app.src.robot.pkg.DTO.robot_dto import RobotDTO
from app.src.robot.pkg.interfaces.gateway_interfaces import RobotGatewayInterface
from app.src.robot.core.usecases.request_useCases import RequestUseCase
class RobotUseCase:
    
    @staticmethod
    def createRobot(robotDTO: RobotDTO, request: Request):

        robot = Robot(robotDTO.brand, 
                      robotDTO.description, 
                      robotDTO.axis_number,
                      [0 for x in range (0, robotDTO.axis_number)],
                      0,
                      request)
        
        return robot
    
    @staticmethod
    def getRobotInfo(robot: Robot, robotGateway: RobotGatewayInterface):
        
        robot.request = RequestUseCase.startCountProcess(robot.request)
        informations = robotGateway.getRobotInformation()
        robot.request = RequestUseCase.stopCountProcess(robot.request)
        
        robot.position = informations[0]
        robot.claw = informations[1]
        robot.data = informations[2]
        return robot