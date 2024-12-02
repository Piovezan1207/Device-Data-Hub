

class Request:
    def __init__(self,
                 id: int,
                 timestemp: int,
                 robot_request_timestemp: int,
                 dt_request_timestemp: int):
        
        if id <= 0:
            raise ValueError("ID must be a positive integer.")
        if timestemp <= 0:
            raise ValueError("Timestamp must be a positive integer.")
        # if robot_request_timestemp <= 0:
        #     raise ValueError("Robot request timestamp must be a positive integer.")
        # if dt_request_timestemp <= 0:
        #     raise ValueError("DT request timestamp must be a positive integer.")
        

        self._id = id
        self._timestemp = timestemp
        self._robot_request_timestemp = robot_request_timestemp
        self._dt_request_timestemp = dt_request_timestemp

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if value <= 0:
            raise ValueError("ID must be a positive integer.")
        self._id = value

    @property
    def timestemp(self) -> int:
        return self._timestemp

    @timestemp.setter
    def timestemp(self, value: int):
        if value <= 0:
            raise ValueError("Timestamp must be a positive integer.")
        self._timestemp = value

    @property
    def robot_request_timestemp(self) -> int:
        return self._robot_request_timestemp

    @robot_request_timestemp.setter
    def robot_request_timestemp(self, value: int):
        if value <= 0:
            raise ValueError("Robot request timestamp must be a positive integer.")
        self._robot_request_timestemp = value

    @property
    def dt_request_timestemp(self) -> int:
        return self._dt_request_timestemp

    @dt_request_timestemp.setter
    def dt_request_timestemp(self, value: int):
        if value <= 0:
            raise ValueError("DT request timestamp must be a positive integer.")
        self._dt_request_timestemp = value