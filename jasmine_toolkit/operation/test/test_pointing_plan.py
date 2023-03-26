import numpy as np

from jasmine_toolkit.operation.pointing_plan import PointingPlan


def test_included_p():
    pp = PointingPlan()
    a = np.array([[0., 0.], [0., 1.], [1., 1.]])
    p = np.array([1.0, 0.0])
    assert not pp.included_p(a, p)
    p = np.array([0.1, 0.1])
    assert pp.included_p(a, p)
