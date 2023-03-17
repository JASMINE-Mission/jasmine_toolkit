import numpy as np


class PointingPlan:
    def __init__(self):
        self.__pointing_entries: np.ndarray = np.array([])

    def add_entry(self, entry: np.ndarray) -> np.ndarray:
        self.__pointing_entries = np.vstack(self.__pointing_entries, entry)

    def get_array(self) -> np.ndarray:
        return self.__pointing_entries.copy()
