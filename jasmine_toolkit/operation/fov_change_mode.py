from enum import Enum


class EnumFovChangeMode(Enum):
    NEW = 0
    VERTICAL = 1
    HORIZONTAL = 2

    @classmethod
    def get_names(cls):
        return [i.name for i in cls]

    @classmethod
    def get_value(cls):
        return [i.value for i in cls]