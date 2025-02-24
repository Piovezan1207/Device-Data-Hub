from dataclasses import dataclass

@dataclass
class RobotDTO: 
    id: int   
    type: str
    brand: str 
    axis: int
