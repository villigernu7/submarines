from enum import Enum


REQUEST_START_GAME = "\x03\x01\x01\x01"
CONFIRM_START_GAME = "\x03\x01\x01\x02"
STOP_GAME = "\x03\x01\x01\x03"

READY_CLIENT_PLAYER = "\x03\x01\x02\x01"
READY_SERVER_PLAYER_HEADER = "\x03\x01\x02"

ATTACK_HEADER = "\x04\x01\x03"
RESPONSE_HEADER = "\x03\x01\x04"


class StartingPlayer(Enum):
    SERVER_PLAYER = "\x02"
    CLIENT_PLAYER = "\x03"


class Result(Enum):
    MISS = 0
    HIT = 1
    DESTROY = 2
    DEFEAT = 3
