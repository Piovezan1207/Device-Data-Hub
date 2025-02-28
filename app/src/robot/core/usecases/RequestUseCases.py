from src.robot.core.entities.Request import Request
from src.robot.core.entities.Robot import Robot
from src.robot.pkg.DTO.RequestDTO import RequestDTO
import time

class RequestUseCase:
    
    @staticmethod
    def createRequest(id: int):
        newRequest = Request(id,
                             time.perf_counter(),
                             0,
                             0)
        
        return newRequest
    
    @staticmethod
    def loadRequest(requestDTO: RequestDTO):
        request = Request(requestDTO.id,
                          requestDTO.timestemp,
                          requestDTO.robot_request_timestemp,
                          0)
        return request
    
    @staticmethod
    def startCountProcess(request: Request):
        request.robot_request_timestemp = time.perf_counter()
        return request

    @staticmethod
    def stopCountProcess(request: Request):
        if request.robot_request_timestemp == 0:
            raise Exception("You must first use 'startCountProcess' function. ")
        request.robot_request_timestemp = (time.perf_counter() - request.robot_request_timestemp) 
        return request
    
    @staticmethod
    def calculateDtRequestTime(request: Request):
        request.dt_request_timestemp = (time.perf_counter() - request.timestemp) - request.robot_request_timestemp
        return request