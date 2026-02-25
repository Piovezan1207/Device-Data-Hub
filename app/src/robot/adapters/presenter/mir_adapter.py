from app.src.robot.pkg.interfaces.adapter_interface import RobotAdapterInterface
from src.robot.core.entities.robot import Robot
from src.robot.core.entities.request import Request

import json

class MirAdapter(RobotAdapterInterface):
    
    def __init__(self):
        super().__init__()
    
    def adaptRobotInformationsToDT(self, robot: Robot):
        robotInformations = {
        "axes": robot.position, 
        "claw_open": robot.claw,
        "data" : robot.data,
        "robot_on": 1,
        "robot" : 
            {
                "brand" : robot.brand,
                "description" : robot.description,
                "axis_number" : robot.axis_number
             },
        "robot_fun_process_time" : robot.request.robot_request_timestemp,
        "request_timestemp" : robot.request.timestemp,
        }
        
        return json.dumps(robotInformations)
      
      
class MirAdapterPt(RobotAdapterInterface):
    
    def __init__(self):
        super().__init__()
    
    def adaptRobotInformationsToDT(self, robot: Robot):
        robotInformations = {
        "Eixos": robot.position, 
        "claw_open": robot.claw,
        "data" : robot.data,
        "robot_on": 1,
        "robot" : 
            {
                "brand" : robot.brand,
                "description" : robot.description,
                "axis_number" : robot.axis_number
             },
        "robot_fun_process_time" : robot.request.robot_request_timestemp,
        "request_timestemp" : robot.request.timestemp,
        }
        
        return json.dumps(robotInformations)
      
