class Robot:
    def __init__(self, 
                 id: int,
                 type: str,
                 axis: int,
                 brand: str): 
        
        self._id = id
        self._brand = brand
        self._type = type
        self._axis = axis


    @property
    def id(self) -> int:
        return self._id

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def type(self) -> str:
        return self._type

    @property
    def axis(self) -> int:
        return self._axis

    
    