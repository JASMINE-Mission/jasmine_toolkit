import jasmine_toolkit.utils.parameters as px
from jasmine_toolkit.utils.parameters import Parameters
import pkg_resources
import math
from pytest import approx
from astropy import units as u


def test_singleton():
    __reset()
    sg = Parameters()
    two = Parameters()
    sg.ready()
    subtract = sg.effective_pupil_diameter - two.effective_pupil_diameter
    assert -0.0001 < subtract.value < 0.0001
    __turn_dirty()
    sg.effective_pupil_diameter = 0.2
    sg.ready()
    assert 0.19999 < two.effective_pupil_diameter < 0.200001
    assert -0.0001 < sg.effective_pupil_diameter\
           - two.effective_pupil_diameter < 0.0001


def test_singleton_2():
    __reset()
    one = Parameters()
    one.effective_pupil_diameter = 0.2
    one.ready()
    two = Parameters()
    assert -0.0001 < one.effective_pupil_diameter - 0.2 < 0.0001


def test_update_from_file():
    p = Parameters()
    __turn_dirty()
    filename = pkg_resources\
        .resource_filename('jasmine_toolkit',
                           'utils/test/constants_update.yaml')
    p.apply(filename)
    p.ready()
    assert p.maneuver_time.value == 12345


def test_update_file_in_not_exists_data():
    p = Parameters()
    __turn_dirty()
    filename = pkg_resources.resource_filename(
        'jasmine_toolkit', 'utils/test/constants_not_exists.yaml')
    try:
        p.apply(filename)
        assert False, 'no guard'
    except AttributeError as e:
        print(e)


def test_dirty_mode():
    p = Parameters()
    __turn_dirty()
    try:
        print(p.EARTH_MASS)
        assert False, 'no guard'
    except RuntimeError as e:
        print(e)
    p.EARTH_MASS = 456
    p.ready()
    assert 456 == p.EARTH_MASS


def test_clean_mode():
    try:
        p = Parameters()
        __turn_clean()
        try:
            p.EARTH_MASS = 456
            assert False, 'no guard'
        except RuntimeError as e:
            print(e)
        print(p.EARTH_MASS)
    finally:
        __reset()


def test_extract_description():
    d1 = {'description': 'hoge'}
    assert 'hoge' == px._extract_description(d1)
    assert '' == px._extract_description({})


def test_extract_unit():
    d1 = {'unit': 'kg'}
    assert 'kg' == px._extract_unit(d1)
    assert '' == px._extract_unit({})


def test_extract_num_value():
    p = Parameters()
    assert type(p._extract_value({'value': '100'})) is int
    assert type(p._extract_value({'value': '5.97'})) is float
    assert type(p._extract_value({'value': '5.9724E24'})) is float
    assert type(p._extract_value({'value': '6.6743E-11'})) is float


def test_extract_not_num_value():
    p = Parameters()
    assert type(p._extract_value({'value': ''})) is str
    assert type(p._extract_value({'value': False})) is bool
    assert type(p._extract_value(
        {'value': "__import__('math').radians(-1.4)"})) is float
    assert type(p._extract_value(
        {'value': "__impo__('math').radians(-1.4)"})) is str


def test_formula():
    p = Parameters()
    p.ready()
    before = p.effective_focal_length
    print(before)
    __turn_dirty()
    p.f_number = 0
    p.ready()
    after = p.effective_focal_length
    print(after)
    assert(before != after)


def test_formulas():
    __reset()
    p = Parameters()
    p.ready()
    p.filter_efficiency
    p.effective_focal_length
    p.average_filter_efficiency
    p.average_telescope_throughput
    p.average_quantum_efficiency
    p.total_efficiency
    p.detector_format_x
    p.detector_format_y
    p.orbital_period
    p.earth_mu
    p.earth_c1
    p.earth_c2
    p.inclination
    p.c_pix
    p.read_time


def test_efficiency():
    __reset()
    # number of mirror = 5, mirror reflection rate = 0.98, QE = 0.8,
    # filter through put = 0.9 is assumed
    sg = Parameters()
    sg.ready()
    assert sg.total_efficiency == approx(0.6136365527435249)


def test_troughput():
    __reset()
    sg = Parameters()
    sg.ready()
    val = sg.average_telescope_throughput
    assert val == approx(0.825825)


def test_period():
    __reset()
    sg = Parameters()
    sg.orbital_altitude = 550000 * u.m
    sg.ready()
    period = sg.orbital_period
    print(period)
    assert 5738 < period.value < 5740


def test_inclination():
    __reset()
    sg = Parameters()
    sg.orbital_altitude = 550000 * u.m
    sg.ready()
    assert 97.5 < math.degrees(sg.inclination.value) < 97.7


def __turn_dirty():
    setattr(Parameters(), '_Parameters__is_dirty', True)


def __turn_clean():
    setattr(Parameters(), '_Parameters__is_dirty', False)


def __reset():
    setattr(Parameters, '_Parameters__instance', None)
