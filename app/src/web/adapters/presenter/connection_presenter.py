from app.src.web.pkg.interfaces.adapter_interfaces import ConnectAdapterInterface

from app.src.web.adapters.presenter.robot_presenter import DefaultRobotPresenter
from app.src.web.adapters.presenter.broker_presenter import DefaultBrokerPresenter


class DefaultConnectionPresenter(ConnectAdapterInterface):
    def __init__(self):
        self._robotAdapter = DefaultRobotPresenter()
        self._brokerAdapter = DefaultBrokerPresenter()
    
    def adaptConnectionInformation(self, connection):
        
        if connection is None:
            return {}
        
        data = {
            "id": connection.id,
            "ip": connection.ip,
            "port": connection.port,
            "description": connection.description,
            "token": connection.token,
            "mqttTopic": connection.mqttTopic,
            "robot": self._robotAdapter.adaptRobotInformation(connection.robot),
            "broker": self._brokerAdapter.adaptBrokerInformation(connection.broker),
            "status": {
                "running" : connection.status.running,
                "connected" : connection.status.connected,
                "error" : connection.status.error,
                "message" : connection.status.message
            }
        }
        
        return data
    
    def adaptConnectionsInformation(self, connections):
        
        if connections is None:
            return {"connections": []}
        
        data = {

                "connections":
                [{
                    "id": connection.id,
                    "ip": connection.ip,
                    "port": connection.port,
                    "description": connection.description,
                    "token": connection.token,
                    "mqttTopic": connection.mqttTopic,
                    "robot": self._robotAdapter.adaptRobotInformation(connection.robot),
                    "broker": self._brokerAdapter.adaptBrokerInformation(connection.broker),
                    "status": {
                                "running" : connection.status.running,
                                "connected" : connection.status.connected,
                                "error" : connection.status.error,
                                "message" : connection.status.message
                            }
                } for connection in connections]
            
        }
        
        return data