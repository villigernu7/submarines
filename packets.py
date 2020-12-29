from enum import Enum


REQUEST_START_GAME = "\x03\x01\x01\x01"
CONFIRM_START_GAME = "\x03\x01\x01\x02"
STOP_GAME = "\x03\x01\x01\x03"

READY_P2 = "\x03\x01\x02\x01"
READY_P1_START_P1 = "\x03\x01\x02\x02"
READY_P1_START_P2 = "\x03\x01\x02\x03"

ATTACK_HEADER = "\x04\x01\x03"
RESPONSE_HEADER = "\x03\x01\x04"


class Result(Enum):
    MISS = 0
    HIT = 1
    DESTROY = 2
    DEFEAT = 3
