from ..DTO.RobotDTO import RobotDTO

from ..interfaces.externalInterfaces import RobotExternalInterface
from ..usecases.RobotUseCases import RobotUseCase
from ..usecases.RequestUseCases import RequestUseCase
from ..gateways.RobotGateway import RobotGateway
from ..interfaces.AdapterInterface import  RobotAdapterInterface

class RobotController:
    
    @staticmethod
    def getRobotInfo(robotDTO: RobotDTO, robotConnection: RobotExternalInterface, robotAdapter: RobotAdapterInterface):
        
        #Cria roo e requisição
        request = RequestUseCase.createRequest(1)
        robot = RobotUseCase.createRobot(robotDTO, request)
        
        robotGateway = RobotGateway(robotConnection)
        
        robotWithPositions = RobotUseCase.getRobotInfo(robot, robotGateway)
        
        
        
        informationToDT = robotAdapter.adaptRobotInformationsToDT(robotWithPositions)
        
        return informationToDT
        
