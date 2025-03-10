from src.robot.pkg.interfaces.externalInterfaces import RobotExternalInterface
import websockets
import threading
import requests
import asyncio
import weakref
import json
import time

import re

class MIRConnection(RobotExternalInterface):
    
    # def __del__(self):
    #     print("Instância foi deletada")
    
    def __init__(self, ip, Authorization):
        self._ip = ip
        self._Authorization = Authorization
        super().__init__()
        self._data = {}
        self.ultima_missao = None
        self.start_position = None
        
        #Cria uma thread com dependencia fraca dessa prorpia classe, a fim de coletar dados de uma conexão webscoket, referente ao ros do mir
        #e colcoar dentro do objeto dessa classe.
        self.wsData = None
        self._selfWeak = weakref.ref(self)
        
        self.threadWs = threading.Thread(target=MIRConnection.run_websocket, args=(self._selfWeak, self._ip, ))
        self.threadWs.start()
        
        
        
    
    def _request(self, endpoint):
        url = f"http://{self._ip}/api/v2.0.0/{endpoint}"
        headers = {'Authorization': self._Authorization, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json() 
        else:
            return None 
            raise Exception("Erro ao pegar dado do mir.")
    
    def _get_guid(self, map_id, name):
        positions = self._request(f"maps/{map_id}/positions")
        return next((p["guid"] for p in positions if p.get("name") == name), None) if positions else None
    
    def getRobotPosition(self) -> list:
        pos, data = self.getStatus()

        self._data = data
       
        return pos
    
    def getClawStatus(self) -> int:
        return 1
    
    def getRobotData(self) -> object:
        return self._data


    def getStatus(self) -> object:
        status = self._request("status")

        if not status: return None
        
        map_id, position = status.get("map_id"), status.get("position", {})

        actual_postion = [position.get("y", 0), position.get("x", 0), position.get("orientation", 0)]

        data = {
                "goal_path": None,
                "start_path": None,
                "battery": None,
                "mission": None,
                "state": None,
                "anchor": None,
                "path" : None
            }    
    
        data["path"] = self.wsData
    
        mission = status.get("mission_text", "")
        data["mission"] = mission
        
        battery = status.get("battery_percentage")
        data["battery"] = battery
        
        state_text = status.get("state_text")
        data["state"] = state_text
        
        match = re.search(r"Moving to '(.*?)'", mission)
        destino = match.group(1) if match else None
        
        guid_anchor = self._get_guid(map_id, "carregador")
        values_anchor = self._request(f"positions/{guid_anchor}") if guid_anchor else {}
        values_anchor = values_anchor.get("pos_y", 0), values_anchor.get("pos_x", 0), values_anchor.get("orientation", 0),"carregador"
        data["anchor"] = values_anchor

        if destino is None: 
            return actual_postion, data
        
        if destino != self.ultima_missao:
            self.ultima_missao, self.start_position = destino, [position.get("y", 0), position.get("x", 0), position.get("orientation", 0),self.ultima_missao]

        guid_goal = self._get_guid(map_id, destino)
        values_goal = self._request(f"positions/{guid_goal}") if guid_goal else {}

        data["goal_path"] = [values_goal.get("pos_y", 0), values_goal.get("pos_x", 0), values_goal.get("orientation", 0),destino]
        data["start_path"] = self.start_position or [position.get("y", 0), position.get("x", 0), position.get("orientation", 0),self.ultima_missao]
        
        return actual_postion, data

    @staticmethod
    async def wsRosConn(weakObj, ip):
        while True:
            obj = None
            try:
                async with websockets.connect("ws://{}:9090".format(ip)) as ws:
                    subscribe_msg = {
                        "op": "subscribe",
                        "topic": "/mirwebapp/web_path"
                    }
                    await ws.send(json.dumps(subscribe_msg))  # ✅ Uso de 'await'

                    while True:
                        obj = weakObj()
                        
                        if obj == None: break
                        
                        mensagem = await ws.recv()  # ✅ Uso de 'await'
                        data = json.loads(mensagem)

                        if "msg" in data:
                            caminho = data["msg"]
                            obj.wsData = [{"x": x, "y": y} for x, y in zip(caminho["x"], caminho["y"])]

                        
                        del obj

            except Exception as e:
                if obj: del obj
                
            obj = weakObj()
            if obj == None: break
            
    @staticmethod
    def run_websocket(weakObj, ip):
        """ Executa a comunicação WebSocket em um loop separado para evitar conflitos com asyncio. """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(MIRConnection.wsRosConn(weakObj, ip))
