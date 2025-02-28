from src.web.core.entities.Broker import Broker

from src.web.pkg.DTO.BrokerDTO import BrokerDTO

from src.web.pkg.interfaces.gatewayInterfaces import DataBaseGatewayInterface

class BrokerUseCases:
    
    @staticmethod
    def create(ip: str,
                port: int,
                user: str, 
                password: str, 
                nickName: str,
                dataBaseGateway: DataBaseGatewayInterface) -> Broker:
        
        brokerDto = dataBaseGateway.createBroker(ip, port, user, password, nickName)
        
        broker = BrokerUseCases.DtoToEntitie(brokerDto)
        
        return broker
    
    @staticmethod
    def getBroker(id: int, dataBaseGateway: DataBaseGatewayInterface) -> Broker:
        brokerDto = dataBaseGateway.getBroker(id)
        
        if brokerDto is None:
            return None
        
        broker = BrokerUseCases.DtoToEntitie(brokerDto)
        
        return broker
    
    @staticmethod
    def getAllBrokers(dataBaseGateway: DataBaseGatewayInterface) -> list[Broker]:
        brokerDtos = dataBaseGateway.getAllBrokers()
        
        if brokerDtos is None:
            return None
        
        brokers = []
        
        for brokerDto in brokerDtos:
            broker = BrokerUseCases.DtoToEntitie(brokerDto)
            brokers.append(broker)
            
        return brokers
    
    @staticmethod
    def deleteBroker(id: int, dataBaseGateway: DataBaseGatewayInterface) -> bool:
        return dataBaseGateway.deleteBroker(id)
    
    @staticmethod
    def DtoToEntitie(brokerDto: BrokerDTO) -> Broker:
        return Broker(brokerDto.id, brokerDto.ip, brokerDto.port, brokerDto.user, brokerDto.password, brokerDto.nickname)