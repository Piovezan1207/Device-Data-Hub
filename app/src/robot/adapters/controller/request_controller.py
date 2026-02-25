from app.src.robot.pkg.DTO.request_dto import RequestDTO
from app.src.robot.core.usecases.request_useCases import RequestUseCase
from app.src.robot.pkg.interfaces.adapter_interface import RequestAdapterInterface

class RequestController:
    
    @staticmethod
    def calculateTime(requestDTO: RequestDTO, requestAdapter: RequestAdapterInterface):
        request = RequestUseCase.loadRequest(requestDTO)
        
        requestWithDtTime = RequestUseCase.calculateDtRequestTime(request)
        dtLatencyInformation =  requestAdapter.adaptRequestInformations(requestWithDtTime)
        
        return(dtLatencyInformation)
        
        