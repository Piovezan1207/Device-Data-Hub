from ..entities.Request import Request

class Robot:
    def __init__(self, brand: str, 
                 description: str,
                 axis_number: int,
                 position: list[int],
                 claw: int,
                 request: Request):
        
        if len(position) != axis_number:
            raise ValueError("The position list must match the number of axes.")
        if claw not in (0, 1):
            raise ValueError("Claw must be 0 (closed) or 1 (open).")
        
        self._brand = brand
        self._description = description
        self._axis_number = axis_number
        self._position = position
        self._claw = claw
        self._request = request

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def description(self) -> str:
        return self._description

    @property
    def axis_number(self) -> int:
        return self._axis_number

    @property
    def position(self) -> list[int]:
        return self._position

    @position.setter
    def position(self, new_position: list[int]):
        if len(new_position) != self._axis_number:
            raise ValueError("New position must match the number of axes.")
        self._position = new_position

    @property
    def claw(self) -> int:
        return self._claw

    @claw.setter
    def claw(self, state: int):
        if state not in (0, 1):
            raise ValueError("Claw state must be 0 (closed) or 1 (open).")
        self._claw = state
    
    @property
    def request(self):
        return self._request
    
    @request.setter
    def request(self, request):
        self._request = request
    
    