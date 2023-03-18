import jasmine_toolkit.utils.parameters2 as px
from jasmine_toolkit.utils.parameters2 import Parameters2
import pkg_resources
import yaml


#def test_dummy():
#    filename = pkg_resources.resource_filename('jasmine_toolkit', 'utils/constants/constants.yaml')
#    print(filename)
#    print(type(filename))
#    print(eval("__import__('math').radians(-1.4)"))
#    with open(filename) as file:
#        obj = yaml.safe_load(file)
#        print(obj)

def test_singleton():
    print("test__sigleton")
    print("new 1")
    p1 = Parameters2()
    assert p1 is not None
    print("new 2")
    p2 = Parameters2()
    assert p1 == p2

def test_dirty_mode():
    p = Parameters2()
    __turn_dirty()
    try:
        d = p.dummy
        assert False, 'no guard'
    except RuntimeError as e:
        print (e)
    p.dummy = 456

def test_clean_mode():
    p = Parameters2()
    __turn_clean()
    try:
        p.dummy = 456
        assert False, 'no guard'
    except RuntimeError as e:
        print (e)
    d = p.dummy

def test_get_yaml_data():
    p = Parameters2()
    p.ready()
#    print(p.EARTH_MASS)

def test_extract_description():
    d1 = {'description':'hoge'}
    assert 'hoge' == px._extract_description(d1)
    assert '' == px._extract_description({})

def test_extract_unit():
    d1 = {'unit':'kg'}
    assert 'kg' == px._extract_unit(d1)
    assert '' == px._extract_unit({})

def test_extract_value():
    assert type(px._extract_value({'value':'100'})) is int
    assert type(px._extract_value({'value':'5.97'})) is float
    assert type(px._extract_value({'value':'5.9724E24'})) is float
    assert type(px._extract_value({'value':False})) is bool
    assert type(px._extract_value({'value':"__import__('math').radians(-1.4)"})) is float
    complex_statement = "__import__('jasmine_toolkit.datamodel.efficiency').datamodel.efficiency.Efficiency.from_json(__import__('pkg_resources').resource_filename('jasmine_toolkit', 'data/qe/qe170.json'))"
    print(type(px._extract_value({'value': complex_statement})))
    print(px._extract_value({'value': complex_statement}))

def __turn_dirty():
    setattr(Parameters2(), '_Parameters2__is_dirty', True)

def __turn_clean():
    setattr(Parameters2(), '_Parameters2__is_dirty', False)

def __reset():
    setattr(Parameters2, '__instance', None)
