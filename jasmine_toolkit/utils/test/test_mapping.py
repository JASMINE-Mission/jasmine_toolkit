import math

import astropy.units as u
from astropy.time import Time, TimeDelta

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.utils.mapping import Mapping


def test_run():
    m = Mapping()
    m.make_data(EnumPointingFreedom.POINTING_FIXED,
                EnumPointingMode.FOUR_FOV_IN_ORBIT,
                Time('2028-01-01T00:00:00', scale="tcb"),
                TimeDelta(0.02 * u.d))


def test_statistics():
    m = Mapping()
    a = [[[]]]
    t = Time('2020-01-01T00:00:00')
    dt = TimeDelta(0.1 * u.yr)
    for i in range(30):
        a[0][0].append([t, 1])
        t = t + dt
    m._Mapping__data = a
    duration = a[0][0][len(a[0][0]) - 1][0] - a[0][0][0][0]
    tc = a[0][0][0][0] + duration * 0.5
    stat = Mapping.calc_statistics(tc, a)
    assert math.isclose(math.sqrt(stat[0][2] * len(a[0][0])), 1.5, abs_tol=0.1)
