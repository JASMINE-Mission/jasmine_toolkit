from jasmine_toolkit.utils.parameters2 import Parameters2

def test_singleton():
    p1 = Parameters2()
    assert p1 is not None
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

def __turn_dirty():
    setattr(Parameters2(), '_Parameters2__is_dirty', True)

def __turn_clean():
    setattr(Parameters2(), '_Parameters2__is_dirty', False)

def __reset():
    setattr(Parameters2, '__instance', None)
