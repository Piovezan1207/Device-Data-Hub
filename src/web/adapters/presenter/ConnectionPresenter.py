from src.web.pkg.interfaces.AdapterInterfaces import ConnectAdapterInterface


class DefaultConnectionPresenter(ConnectAdapterInterface):
    def __init__(self):
        pass
    
    def adaptConnectionInformation(self, connection):
        data = {
            "connection" : {
            "id": connection.id,
            "ip": connection.ip,
            "port": connection.port,
            "description": connection.description,
            "token": connection.token,
            "mqttTopic": connection.mqttTopic,
            "robot": connection.robot,
            "sender": connection.sender,
            "status": {
                "running" : connection.status.running,
                "connected" : connection.status.connected,
                "error" : connection.status.error,
                "message" : connection.status.message
            }
            }
        }
        
        return data
    
    def adaptConnectionsInformation(self, connections):
        data = {
            "connections": [
                {
                    "id": connection.id,
                    "ip": connection.ip,
                    "port": connection.port,
                    "description": connection.description,
                    "token": connection.token,
                    "mqttTopic": connection.mqttTopic,
                    "robot": connection.robot,
                    "sender": connection.sender,
                    "status": {
                                "running" : connection.status.running,
                                "connected" : connection.status.connected,
                                "error" : connection.status.error,
                                "message" : connection.status.message
                            }
                } for connection in connections
            ]
        }
        
        return data