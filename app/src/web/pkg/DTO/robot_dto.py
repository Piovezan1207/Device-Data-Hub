from dataclasses import dataclass

@dataclass
class RobotDTO: 
    id: int   
    type: str
    axis: int
    brand: str 
