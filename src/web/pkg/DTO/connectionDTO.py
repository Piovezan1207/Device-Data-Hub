from dataclasses import dataclass

@dataclass
class ConnectionDTO:
    id: int
    ip: str 
    port: int
    description: str 
    token: str 
    mqttTopic: str 
    robotId: int
    

