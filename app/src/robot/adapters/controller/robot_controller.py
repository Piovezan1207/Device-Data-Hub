from app.src.robot.pkg.DTO.robot_dto import RobotDTO

from app.src.robot.pkg.interfaces.external_interfaces import RobotExternalInterface
from app.src.robot.core.usecases.robot_use_cases import RobotUseCase
from app.src.robot.core.usecases.request_useCases import RequestUseCase
from app.src.robot.adapters.gateway.robot_gateway import RobotGateway
from app.src.robot.pkg.interfaces.adapter_interface import RobotAdapterInterface

class RobotController:
    
    @staticmethod
    def getRobotInfo(robotDTO: RobotDTO, robotConnection: RobotExternalInterface, robotAdapter: RobotAdapterInterface):
        
        #Cria roo e requisição
        request = RequestUseCase.createRequest(1)
        # print(request.id, robotDTO.brand, request)
        robot = RobotUseCase.createRobot(robotDTO, request)
        # print(robot.request , "ue")
        robotGateway = RobotGateway(robotConnection)
        
        robotWithPositions = RobotUseCase.getRobotInfo(robot, robotGateway)
        
        
        
        informationToDT = robotAdapter.adaptRobotInformationsToDT(robotWithPositions)
        
        return informationToDT
        
