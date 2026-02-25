from app.src.web.pkg.interfaces.adapter_interfaces import RobotAdapterInterface

class DefaultRobotPresenter(RobotAdapterInterface):
    def __init__(self):
        pass
    
    def adaptRobotInformation(self, robot):
        
        if robot is None:
            return {}
        
        data = {
            "id": robot.id,
            "type": robot.type,
            "axis": robot.axis,
            "brand": robot.brand
        }
        
        return data
        
    def adaptRobotsInformation(self, robots):
        
        if robots is None:
            return {"robots" : []}
        
        data = {
                "robots" : [{
                    "id": robot.id,
                    "type": robot.type,
                    "axis": robot.axis,
                    "brand": robot.brand
                } for robot in robots]
        }
        
        return data