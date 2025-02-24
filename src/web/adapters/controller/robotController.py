from src.web.core.usecases.RobotUseCases import RobotUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway
from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface

from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface

class robotController:
    @staticmethod
    def getAllRobots(dataBaseExternal: DataBaseExternalInterface):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robots = RobotUseCases.getAllRobots(databaseGateway)

        return robots  #Adicionar adapter!!
    
    @staticmethod
    def getRobot(id, dataBaseExternal: DataBaseExternalInterface):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robot = RobotUseCases.getRobot(id, databaseGateway)
        
        return robot #Adicionar adapter!!
        
        
    
    @staticmethod
    def createRobot(typeR, axis, brand, dataBaseExternal: DataBaseExternalInterface):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        robot = RobotUseCases.create(typeR, axis, brand, databaseGateway)
        
        return robot #Adicionar adapter!!
    
    @staticmethod
    def deleteRobot(id, dataBaseExternal: DataBaseExternalInterface):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        deleted = RobotUseCases.deleteRobot(id, databaseGateway)
        
        return deleted  #Adicionar adapter!!