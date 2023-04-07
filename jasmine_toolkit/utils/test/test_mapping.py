import astropy.units as u
from astropy.time import Time, TimeDelta

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.utils.mapping import Mapping


def test_run():
    m = Mapping()
    m.run(EnumPointingFreedom.POINTING_FIXED,
          EnumPointingMode.FOUR_FOV_IN_ORBIT,
          Time('2028-01-01T00:00:00', scale="tcb"),
          TimeDelta(0.02 * u.d))


def test_statistics():
    m = Mapping()
    a = [[]]
    t = Time('2020-01-01T00:00:00')
    dt = TimeDelta(0.1 * u.yr)
    for i in range(30):
        a.append([Time()])
    m._Mapping__data = a
    print(m._Mapping__data)
