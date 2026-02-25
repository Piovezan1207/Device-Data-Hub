from app.src.web.core.usecases.broker_use_cases import BrokerUseCases

from app.src.web.adapters.gateway.data_base_gateway import DataBaseGateway

from app.src.web.pkg.interfaces.external_interfaces import DataBaseExternalInterface

from app.src.web.pkg.interfaces.adapter_interfaces import BrokerAdapterInterface
from app.src.web.adapters.presenter.broker_presenter import DefaultBrokerPresenter

class BrokerController:
    @staticmethod
    def getAllBrokers(dataBaseExternal: DataBaseExternalInterface, brokerAdapter: BrokerAdapterInterface = DefaultBrokerPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        brokers = BrokerUseCases.getAllBrokers(databaseGateway)

        adapter = brokerAdapter()

        return adapter.adaptBrokersInformation(brokers)
    
    @staticmethod
    def getBroker(id, dataBaseExternal: DataBaseExternalInterface, brokerAdapter: BrokerAdapterInterface = DefaultBrokerPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        broker = BrokerUseCases.getBroker(id, databaseGateway)
        
        adapter = brokerAdapter()
        
        return adapter.adaptBrokerInformation(broker)
        
        
    
    @staticmethod
    def createBroker(ip: str, port: int, user: str, password: str, nickname: str, dataBaseExternal: DataBaseExternalInterface, brokerAdapter: BrokerAdapterInterface = DefaultBrokerPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        broker = BrokerUseCases.create(ip, port, user, password, nickname, databaseGateway)
        
        adapter = brokerAdapter()
        
        return adapter.adaptBrokerInformation(broker)
    
    @staticmethod
    def deleteBroker(id, dataBaseExternal: DataBaseExternalInterface, brokerAdapter: BrokerAdapterInterface = DefaultBrokerPresenter):
        
        databaseGateway = DataBaseGateway(dataBaseExternal)
        
        deleted = BrokerUseCases.deleteBroker(id, databaseGateway)
        
        adapter = brokerAdapter()
        
        return adapter.adaptBrokerInformation(deleted)