import enum


class CleanState(enum.Enum):
    tables = 0
    file = 1
    chunk = 2

    default = 0
