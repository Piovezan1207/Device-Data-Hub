from src.robot.pkg.interfaces.externalInterfaces import RobotExternalInterface


class KukaKR203Connection(RobotExternalInterface):
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port

    def getRobotPosition(self) -> list:
        position = [0,1,2,3,4,5]
        return position

    def getClawStatus(self) -> int:
        return 1
        pass


    def getRobotData(self) -> object:
            return {"Robot" : "KR203"}