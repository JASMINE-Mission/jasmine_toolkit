import math
import random

from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.time import Time

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.satellite.attitude.attitude import Attitude


def test_position_angle():
    a: Attitude = Attitude(EnumPointingFreedom.POINTING_FIXED)
    coord = SkyCoord(lon=90.0 * u.deg, lat=0.0 * u.deg,
                     frame='barycentricmeanecliptic')
    time = Time('2022-03-21T00:00:00')
    pa = a.get_position_angle(coord, time)
    assert math.isclose(pa, 1.57, abs_tol=0.01)


def test_position_angle_over_pi():
    a: Attitude = Attitude(EnumPointingFreedom.POINTING_FIXED)
    coord = SkyCoord(lon=90.0 * u.deg, lat=0.0 * u.deg,
                     frame='barycentricmeanecliptic')
    time = Time('2022-09-23T00:00:00')
    pa = a.get_position_angle(coord, time)
    assert math.isclose(pa, 4.71, abs_tol=0.01)


def test_position_angle_over_random(monkeypatch):
    monkeypatch.setattr(random, 'random', lambda : 1)
    a: Attitude = Attitude(EnumPointingFreedom.POINTING_RANDOM)
    coord = SkyCoord(lon=90.0 * u.deg, lat=0.0 * u.deg,
                     frame='barycentricmeanecliptic')
    time = Time('2022-02-05T00:00:00')
    pa = a.get_position_angle(coord, time)
    assert math.isclose(pa, 2.33, abs_tol=0.005)
