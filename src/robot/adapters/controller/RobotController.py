from src.robot.pkg.DTO.RobotDTO import RobotDTO

from src.robot.pkg.interfaces.externalInterfaces import RobotExternalInterface
from src.robot.core.usecases.RobotUseCases import RobotUseCase
from src.robot.core.usecases.RequestUseCases import RequestUseCase
from src.robot.adapters.gateway.RobotGateway import RobotGateway
from src.robot.pkg.interfaces.AdapterInterface import RobotAdapterInterface

class RobotController:
    
    @staticmethod
    def getRobotInfo(robotDTO: RobotDTO, robotConnection: RobotExternalInterface, robotAdapter: RobotAdapterInterface):
        
        #Cria roo e requisição
        request = RequestUseCase.createRequest(1)
        print(request.id, robotDTO.brand, request)
        robot = RobotUseCase.createRobot(robotDTO, request)
        print(robot.request , "ue")
        robotGateway = RobotGateway(robotConnection)
        
        robotWithPositions = RobotUseCase.getRobotInfo(robot, robotGateway)
        
        
        
        informationToDT = robotAdapter.adaptRobotInformationsToDT(robotWithPositions)
        
        return informationToDT
        
