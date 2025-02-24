from src.robot.pkg.interfaces.gatewayInterfaces import RobotGatewayInterface
from src.robot.pkg.interfaces.externalInterfaces import RobotExternalInterface

class RobotGateway(RobotGatewayInterface):
    
    def __init__(self, robotConnection: RobotExternalInterface):
        super().__init__()
        self._robotConnection = robotConnection
    
    def getRobotInformation(self):
        positions = self._robotConnection.getRobotPosition()
        claw = self._robotConnection.getClawStatus()
        
        return  positions, claw

