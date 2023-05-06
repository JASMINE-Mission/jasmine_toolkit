import jasmine_toolkit.utils.parameters2 as px
from jasmine_toolkit.utils.parameters2 import Parameters2
import pkg_resources



def test_singleton():
    p1 = Parameters2()
    assert p1 is not None
    p2 = Parameters2()
    assert p1 == p2


def test_update_from_file():
    p = Parameters2()
    __turn_dirty()
    filename = pkg_resources.resource_filename('jasmine_toolkit', 'utils/test/constants_update.yaml')
    p.apply(filename)
    p.ready()
    assert p.maneuver_time.value == 12345


def test_update_file_in_not_exists_data():
    p = Parameters2()
    __turn_dirty()
    filename = pkg_resources.resource_filename(
        'jasmine_toolkit', 'utils/test/constants_not_exists.yaml')
    try:
        p.apply(filename)
        assert False, 'no guard'
    except AttributeError as e:
        print(e)


def test_dirty_mode():
    p = Parameters2()
    __turn_dirty()
    try:
        print(p.EARTH_MASS)
        assert False, 'no guard'
    except RuntimeError as e:
        print (e)
    p.EARTH_MASS = 456
    p.ready()
    assert 456 == p.EARTH_MASS


def test_clean_mode():
    try:
        p = Parameters2()
        __turn_clean()
        try:
            p.EARTH_MASS = 456
            assert False, 'no guard'
        except RuntimeError as e:
            print (e)
        print(p.EARTH_MASS)
    finally:
        __reset()


def test_extract_description():
    d1 = {'description':'hoge'}
    assert 'hoge' == px._extract_description(d1)
    assert '' == px._extract_description({})


def test_extract_unit():
    d1 = {'unit':'kg'}
    assert 'kg' == px._extract_unit(d1)
    assert '' == px._extract_unit({})


def test_extract_value():
    p = Parameters2()
    assert type(p._extract_value({'value':''})) is str
    assert type(p._extract_value({'value':'100'})) is int
    assert type(p._extract_value({'value':'5.97'})) is float
    assert type(p._extract_value({'value':'5.9724E24'})) is float
    assert type(p._extract_value({'value':'6.6743E-11'})) is float
    assert type(p._extract_value({'value':False})) is bool
    assert type(p._extract_value({'value':"__import__('math').radians(-1.4)"})) is float
    assert type(p._extract_value({'value':"__impo__('math').radians(-1.4)"})) is str
    # complex_statement = "__import__('jasmine_toolkit.datamodel.efficiency').datamodel.efficiency.Efficiency.from_json(__import__('pkg_resources').resource_filename('jasmine_toolkit', 'data/qe/qe170.json'))"
    # print(type(px._extract_value({'value': complex_statement})))
    # print(px._extract_value({'value': complex_statement}))


def test_specificated_property():
    p = Parameters2()
    p.ready()
    print(p.average_filter_efficiency)


def test_formula():
    p = Parameters2()
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
    p = Parameters2()
    p.ready()
    p.filter_efficiency
    p.effective_focal_length
    p.average_filter_efficiency
    #p.average_telescope_throughput
    #p.average_quantum_efficiency
    #p.total_efficiency
    p.detector_format_x
    p.detector_format_y
    p.orbital_period
    p.earth_mu
    p.earth_c1
    p.earth_c2
    p.inclination
    p.c_pix
    p.read_time

def __turn_dirty():
    setattr(Parameters2(), '_Parameters2__is_dirty', True)

def __turn_clean():
    setattr(Parameters2(), '_Parameters2__is_dirty', False)

def __reset():
    setattr(Parameters2, '__instance', None)
