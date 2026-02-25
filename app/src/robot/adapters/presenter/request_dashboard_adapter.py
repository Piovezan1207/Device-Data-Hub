from app.src.robot.pkg.interfaces.adapter_interface import RequestAdapterInterface
from src.robot.core.entities.request import Request

import json

class RequestDashboardAdapter(RequestAdapterInterface):
    def __init__(self):
        super().__init__()
        
    def adaptRequestInformations(self, request: Request):
        requestInformations = {
        "dt_latency": request.dt_request_timestemp, 
        "robot_fun_process_time" : request.robot_request_timestemp
        }
        
        return json.dumps(requestInformations)