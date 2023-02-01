import numpy as np


class PointingPlan:
    def __init__(self):
        self.pointing_entries: np.ndarray = np.array([])

    def add_entry(self, entry: np.ndarray) -> np.ndarray:
        np.vstack(self.pointing_entries, entry)

    def get_array(self) -> np.ndarray:
        return self.pointing_entries
