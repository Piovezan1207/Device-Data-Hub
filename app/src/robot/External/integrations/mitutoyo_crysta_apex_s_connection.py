from app.src.robot.pkg.interfaces.external_interfaces import RobotExternalInterface


class MitutoyoCrystaApexSConnection(RobotExternalInterface):
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port

    def getRobotPosition(self) -> list:
        position = [0,1,2]
        return position

    def getClawStatus(self) -> int:
        return 1
        pass


    def getRobotData(self) -> object:
            return {"Device" : "CRYSTAL APEX"}