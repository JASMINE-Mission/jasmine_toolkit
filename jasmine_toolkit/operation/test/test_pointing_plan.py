import math
import time

import numpy as np
import pytest

from jasmine_toolkit.operation.pointing_plan import PointingPlan


# TODO
#   Tests for the following methods are not implemented.
#   add_entry, get_array, find_next_pointing, pointing_by_small_maneuver,
#   make_observation, and _get_field_of_view.

@pytest.fixture(scope='module')
def pointing_plan():
    return PointingPlan()


def test_included_p(pointing_plan):
    a = np.array([[0., 0.], [0., 1.], [1., 1.]])
    p = np.array([1.0, 0.0])
    assert not pointing_plan.included_p(a, p)
    p = np.array([0.1, 0.1])
    assert pointing_plan.included_p(a, p)


def test_coord_to_grid(pointing_plan):
    coord = pointing_plan._grid_to_coord(10, 11)
    l0, b0 = pointing_plan._coord_to_grid(coord)
    assert l0 == 10
    assert b0 == 11


def test_grid_to_coord(pointing_plan):
    coord0 = pointing_plan._grid_to_coord(100, 100)
    assert coord0.galactic.l.deg == 0.0
    assert coord0.galactic.b.deg == 0.0
    coord1 = pointing_plan._grid_to_coord(10, 10)
    assert math.isclose(coord1.galactic.l.deg, 359.033, abs_tol=0.01)
    assert math.isclose(coord1.galactic.b.deg, -0.167, abs_tol=0.01)
