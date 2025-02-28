class Broker:
    def __init__(self, 
                    id: int,
                    ip: str,
                    port: int,
                    user: str,
                    password: str,
                    nickname: str = None):
        
        self._id = id
        self._ip = ip
        self._port = port
        self._user = user
        self._password = password
        self._nickname = nickname

    @property
    def id(self):
        return self._id
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def port(self):
        return self._port
    
    @property
    def user(self):
        return self._user
    
    @property
    def password(self):
        return self._password
    
    @property
    def nickname(self):
        return self._nickname
