from app.src.robot.pkg.interfaces.gateway_interfaces import RobotGatewayInterface
from app.src.robot.pkg.interfaces.external_interfaces import RobotExternalInterface

class RobotGateway(RobotGatewayInterface):
    
    def __init__(self, robotConnection: RobotExternalInterface):
        super().__init__()
        self._robotConnection = robotConnection
    
    def getRobotInformation(self):
        positions = self._robotConnection.getRobotPosition()
        claw = self._robotConnection.getClawStatus()
        data = self._robotConnection.getRobotData()
        
        return  positions, claw, data

