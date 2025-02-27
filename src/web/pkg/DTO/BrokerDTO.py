        
from dataclasses import dataclass

@dataclass
class BrokerDTO:

        id: int
        ip: str
        port: int
        user: str
        password: str
        nickname: str