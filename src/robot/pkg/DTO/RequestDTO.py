from dataclasses import dataclass

@dataclass
class RequestDTO:    
    id: int
    timestemp: int
    robot_request_timestemp: int

