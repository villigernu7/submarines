

class BaseGameException(BaseException):
    pass


class StartGameException(BaseGameException):
    pass


class GameFlowException(BaseGameException):
    pass


class IllegalArgumentException(BaseGameException):
    pass
