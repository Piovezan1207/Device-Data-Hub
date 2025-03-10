from src.robot.pkg.interfaces.externalInterfaces import RobotExternalInterface
import requests
import json
import time

import re

class MIRConnection(RobotExternalInterface):
    
    def __init__(self, ip, Authorization):
        self._ip = ip
        self._Authorization = Authorization
        super().__init__()
    
    def _request(self, endpoint):
        url = f"http://{self._ip}/api/v2.0.0/{endpoint}"
        headers = {'Authorization': self._Authorization, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else None

    
    def getRobotPosition(self) -> list:
        url = "http://{}/api/v2.0.0/status".format(self._ip)
        payload = ""
        headers = {
        'Authorization': self._Authorization,
        'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers, data=payload, timeout=5)

        values = json.loads(response.text)
        values = values["position"]
        # print(values)
        
        return[values["y"], values["x"], values["orientation"]]
        
    
    def getClawStatus(self) -> int:
        return 1
    
    def getRobotData(self) -> object:
        status = self._request("status")
        # print(status)
        if not status: return None
        map_id, values = status.get("map_id"), status.get("position", {})

        mission = status.get("mission_text", "")
        
        battery = status.get("battery_percentage")
        
        state_text = status.get("state_text")
        
        match = re.search(r"Moving to '(.*?)'", mission)
        destino = match.group(1) if match else None
        
        guid_anchor = self._get_guid(map_id, "carregador")
        
        values_anchor = self._request(f"positions/{guid_anchor}") if guid_anchor else {}
        
        values_anchor = values_anchor.get("pos_y", 0), values_anchor.get("pos_x", 0), values_anchor.get("orientation", 0),"carregador"

        if destino is None: 
            return [[values.get("y", 0), values.get("x", 0), values.get("orientation", 0)]
                    ,None
                    ,None,
                    battery,
                    mission,
                    state_text,
                    values_anchor]
        
            data = {
                 "goal_path": None,
                "start_path": None,
                "battery": battery,
                "mission": mission,
                "state": state_text,
                "anchor": values_anchor,
            }
        
        if destino != self.ultima_missao:
            self.ultima_missao, self.start_position = destino, [values.get("y", 0), values.get("x", 0), values.get("orientation", 0),self.ultima_missao]

        guid_goal = self._get_guid(map_id, destino)
        
        values_goal = self._request(f"positions/{guid_goal}") if guid_goal else {}

        return [
            [values.get("y", 0), values.get("x", 0), values.get("orientation", 0)],
            [values_goal.get("pos_y", 0), values_goal.get("pos_x", 0), values_goal.get("orientation", 0),destino],
            
            self.start_position or [values.get("y", 0), values.get("x", 0), values.get("orientation", 0),self.ultima_missao],
            
            battery,
            
            mission,state_text, 
            
            values_anchor,
        ]