from ..entities.Robot import Robot
from ..entities.Request import Request
from ..DTO.RobotDTO import RobotDTO
from ..interfaces.gatewayInterfaces import RobotGatewayInterface
from ..usecases.RequestUseCases import RequestUseCase
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
        return robot