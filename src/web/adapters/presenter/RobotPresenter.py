from src.web.pkg.interfaces.AdapterInterfaces import RobotAdapterInterface

class DefaultRobotPresenter(RobotAdapterInterface):
    def __init__(self):
        pass
    
    def adaptRobotInformation(self, robot):
        data = {
            "robot" : { 
            "id": robot.id,
            "type": robot.type,
            "axis": robot.axis,
            "brand": robot.brand
            }
        }
        
        return data
        
    def adaptRobotsInformation(self, robots):
        data = {
            "robots": [
                {
                    "id": robot.id,
                    "type": robot.type,
                    "axis": robot.axis,
                    "brand": robot.brand
                } for robot in robots
            ]
        }
        
        return data