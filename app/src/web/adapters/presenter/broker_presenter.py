from app.src.web.pkg.interfaces.adapter_interfaces import BrokerAdapterInterface
from src.web.core.entities.broker import Broker

class DefaultBrokerPresenter(BrokerAdapterInterface):
    def __init__(self):
        pass
    
    def adaptBrokerInformation(self, broker: Broker):
        
        if broker is None:
            return {}
        
        data = {
            "id": broker.id,
            "ip": broker.ip,
            "port"  : broker.port,
            "user": broker.user,
            "password": broker.password,
            "nickname": broker.nickname
        }
        
        return data
        
    def adaptBrokersInformation(self, brokers ):
        
        if brokers is None:
            return {"brokers" : []}
        
        data = {
                "brokers" : [{
                    "id": broker.id,
                    "ip": broker.ip,
                    "port"  : broker.port,
                    "user": broker.user,
                    "password": broker.password,
                    "nickname": broker.nickname
                } for broker in brokers]
        }
        
        return data