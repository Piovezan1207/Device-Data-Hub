from ..interfaces.AdapterInterface import RobotAdapterInterface
from ..entities.Robot import Robot
from ..entities.Request import Request

import json

class YaskawaRobotAdapter(RobotAdapterInterface):
    
    def __init__(self):
        super().__init__()
    
    def adaptRobotInformationsToDT(self, robot: Robot):
        robotInformations = {
        "axis": robot.position, 
        "claw_open": robot.claw,
        "robot_on": 1,
        "robot" : 
            {
                "brand" : robot.brand,
                "description" : robot.description,
                "axis_number" : robot.axis_number
             },
        "robot_fun_process_time" : robot.request.robot_request_timestemp,
        "request_timestemp" : robot.request.timestemp
        
        }
        
        return json.dumps(robotInformations)