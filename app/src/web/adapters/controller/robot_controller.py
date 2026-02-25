from app.src.web.core.usecases.robot_use_cases import RobotUseCases

from app.src.web.adapters.gateway.data_base_gateway import DataBaseGateway
from app.src.web.pkg.interfaces.gateway_interfaces import DataBaseGatewayInterface

from app.src.web.pkg.interfaces.external_interfaces import DataBaseExternalInterface

from app.src.web.pkg.interfaces.adapter_interfaces import RobotAdapterInterface
from app.src.web.adapters.presenter.robot_presenter import DefaultRobotPresenter
#
class RobotController:
    @staticmethod
    def getAllRobots(dataBaseExternal: DataBaseExternalInterface, robotAdapter: RobotAdapterInterface = DefaultRobotPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robots = RobotUseCases.getAllRobots(databaseGateway)

        adapter = robotAdapter()

        return adapter.adaptRobotsInformation(robots)
    
    @staticmethod
    def getRobot(id, dataBaseExternal: DataBaseExternalInterface, robotAdapter: RobotAdapterInterface = DefaultRobotPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robot = RobotUseCases.getRobot(id, databaseGateway)
        
        adapter = robotAdapter()
        
        return adapter.adaptRobotInformation(robot)
        
        
    
    @staticmethod
    def createRobot(typeR, axis, brand, dataBaseExternal: DataBaseExternalInterface, robotAdapter: RobotAdapterInterface = DefaultRobotPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robot = RobotUseCases.create(typeR, axis, brand, databaseGateway)
        
        adapter = robotAdapter()
        
        return adapter.adaptRobotInformation(robot)
    
    @staticmethod
    def deleteRobot(id, dataBaseExternal: DataBaseExternalInterface, robotAdapter: RobotAdapterInterface = DefaultRobotPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        deleted = RobotUseCases.deleteRobot(id, databaseGateway)
        
        adapter = robotAdapter()
        
        return adapter.adaptRobotInformation(deleted)