from src.robot.pkg.DTO.RequestDTO import RequestDTO
from src.robot.core.usecases.RequestUseCases import RequestUseCase
from src.robot.pkg.interfaces.AdapterInterface import RequestAdapterInterface

class RequestController:
    
    @staticmethod
    def calculateTime(requestDTO: RequestDTO, requestAdapter: RequestAdapterInterface):
        request = RequestUseCase.loadRequest(requestDTO)
        
        requestWithDtTime = RequestUseCase.calculateDtRequestTime(request)
        dtLatencyInformation =  requestAdapter.adaptRequestInformations(requestWithDtTime)
        
        return(dtLatencyInformation)
        
        