from src.web.core.usecases.RobotUseCases import RobotUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway
from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface

from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface

from src.web.pkg.interfaces.AdapterInterfaces import RobotAdapterInterface
from src.web.adapters.presenter.RobotPresenter import DefaultRobotPresenter

class robotController:
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