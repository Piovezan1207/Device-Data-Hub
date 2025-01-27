from ..interfaces.externalInterfaces import RobotExternalInterface
import requests
import json
import time


class MIRConnection(RobotExternalInterface):
    
    def __init__(self, ip, Authorization):
        self._ip = ip
        self._Authorization = Authorization
        super().__init__()
    
    def getRobotPosition(self) -> list:
        url = "http://{}/api/v2.0.0/status".format(self._ip)
        payload = ""
        headers = {
        'Authorization': self._Authorization,
        'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)

        values = json.loads(response.text)
        values = values["position"]
        # print(values)
        
        return[values["y"], values["x"], values["orientation"]]
        
    
    def getClawStatus(self) -> int:
        return 1