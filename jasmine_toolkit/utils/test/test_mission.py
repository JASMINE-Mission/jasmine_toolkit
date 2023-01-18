import math

from pytest import approx
from jasmine_toolkit.utils.parameters import Parameters


def test_singleton():
    sg = Parameters.get_instance()
    two = Parameters.get_instance()
    assert -0.0001 < sg.effective_pupil_diameter - two.effective_pupil_diameter < 0.0001
    sg.set_effective_pupil_diameter(0.2)
    assert 0.19999 < two.effective_pupil_diameter < 0.200001
    assert -0.0001 < sg.effective_pupil_diameter - two.effective_pupil_diameter < 0.0001


def test_singleton_2():
    one = Parameters.get_instance()
    one.set_effective_pupil_diameter(0.2)
    two = Parameters.get_instance()
    assert -0.0001 < one.effective_pupil_diameter - 0.2 < 0.0001


def test_efficiency():
    # number of mirror = 5, mirror reflection rate = 0.98, QE = 0.8, filter through put = 0.9 is assumed
    sg = Parameters.get_instance()
    assert sg.total_efficiency == approx(0.6136365527435249)


def test_troughput():
    sg = Parameters.get_instance()
    val = sg.average_telescope_throughput
    assert val == approx(0.825825)


def test_period():
    sg = Parameters.get_instance()
    sg.set_orbital_altitude(550000)
    assert 5738 < sg.orbital_period < 5740


def test_inclination():
    sg = Parameters.get_instance()
    sg.set_orbital_altitude(550000)
    assert 97.5 < math.degrees(sg.inclination) < 97.7
