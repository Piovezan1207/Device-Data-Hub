from ..DTO.RequestDTO import RequestDTO
from ..usecases.RequestUseCases import RequestUseCase
from ..interfaces.AdapterInterface import RequestAdapterInterface

class RequestController:
    
    @staticmethod
    def calculateTime(requestDTO: RequestDTO, requestAdapter: RequestAdapterInterface):
        request = RequestUseCase.loadRequest(requestDTO)
        
        requestWithDtTime = RequestUseCase.calculateDtRequestTime(request)
        dtLatencyInformation =  requestAdapter.adaptRequestInformations(requestWithDtTime)
        
        return(dtLatencyInformation)
        
        