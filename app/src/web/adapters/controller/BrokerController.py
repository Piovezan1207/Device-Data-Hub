from src.web.core.usecases.BrokerUseCases import BrokerUseCases

from src.web.adapters.gateway.DataBaseGateway import DataBaseGateway

from src.web.pkg.interfaces.externalInterfaces import DataBaseExternalInterface

from src.web.pkg.interfaces.AdapterInterfaces import BrokerAdapterInterface
from src.web.adapters.presenter.BrokerPresenter import DefaultBrokerPresenter

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