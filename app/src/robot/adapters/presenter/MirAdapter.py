from src.robot.pkg.interfaces.AdapterInterface import RobotAdapterInterface
from src.robot.core.entities.Robot import Robot
from src.robot.core.entities.Request import Request

import json

class MirAdapter(RobotAdapterInterface):
    
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
        "request_timestemp" : robot.request.timestemp,
        
        "goal_path": [
    9.4,
    16.75,
    26.565,
    "P_Pedro"
  ],
  "start_path": [
    9.883465766906738,
    18.737468719482422,
    -0.039404213428497314,
    "saida"
  ],
  "battery": 44.599998474121094,
  "mission": "Moving to 'P_Pedro' (1.5 meters to goal)",
  "state": "Executing",
  "anchor": [
    8.773,
    17.958,
    -89.483,
    "carregador"
  ],
  "path": [
    {
      "x": 18.725000381469727,
      "y": 9.875
    },
    {
      "x": 18.503700256347656,
      "y": 9.690400123596191
    },
    {
      "x": 18.261899948120117,
      "y": 9.578200340270996
    },
    {
      "x": 17.975000381469727,
      "y": 9.52500057220459
    },
    {
      "x": 17.69930076599121,
      "y": 9.520500183105469
    },
    {
      "x": 17.449600219726562,
      "y": 9.44379997253418
    },
    {
      "x": 17.17500114440918,
      "y": 9.375
    },
    {
      "x": 16.904699325561523,
      "y": 9.38640022277832
    },
    {
      "x": 16.75,
      "y": 9.399999618530273
    }
  ]
        
        }
        
        return json.dumps(robotInformations)