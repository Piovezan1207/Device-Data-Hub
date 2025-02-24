class Sender:
    def __init__(self, ip: str,
                       port: int,
                       client: object):
        
        self._ip = ip
        self._port = port
        self._client = client
        self._status = "disconnected"
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def port(self):
        return self._port
    
    @property
    def client(self):
        return self._client
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: str):
        self._status = status