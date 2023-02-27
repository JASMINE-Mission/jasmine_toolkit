from enum import Enum


class EnumPointingMode(Enum):
    FOUR_FOV_IN_ORBIT = 4
    SIX_FOV_IN_ORBIT = 6
    EIGHT_FOV_IN_ORBIT = 8

    @classmethod
    def get_names(cls):
        return [i.name for i in cls]

    @classmethod
    def get_values(cls):
        return [i.value for i in cls]