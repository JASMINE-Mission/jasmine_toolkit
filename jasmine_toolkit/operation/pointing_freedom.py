from enum import Enum


class EnumPointingFreedom(Enum):
    POINTING_FIXED = 0
    POINTING_RANDOM = 1

    @classmethod
    def get_names(cls):
        return [i.name for i in cls]

    @classmethod
    def get_values(cls):
        return [i.value for i in cls]