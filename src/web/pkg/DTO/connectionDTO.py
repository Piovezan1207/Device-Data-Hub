from dataclasses import dataclass

@dataclass
class ConnectionDTO:
    id: int
    robotId: int
    mqttTopic: str 
    ip: str 
    port: int
    description: str 
    token: str 
    

