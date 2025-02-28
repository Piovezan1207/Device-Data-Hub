class Status:
    def __init__(self,
                 running: bool,
                 connected: bool,
                 error: bool,
                 message: str):
    
        self._running = running
        self._connected = connected
        self._error = error
        self._message = message
        
    @property
    def running(self) -> bool:
        return self._running
    
    @running.setter
    def running(self, running: bool):
        self._running = running
        
    @property
    def connected(self) -> bool:
        return self._connected
    
    @connected.setter
    def connected(self, connected: bool):
        self._connected = connected
        
    @property
    def error(self) -> bool:
        return self._error
    
    @error.setter
    def error(self, error: bool):
        self._error = error
        
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, message: str):
        self._message = message
        
        
        
    
    
    
