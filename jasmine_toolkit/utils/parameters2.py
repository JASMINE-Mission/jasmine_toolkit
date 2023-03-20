from astropy.constants import Constant
import pkg_resources
import yaml
import codecs


# TODO 規格の切り返したい場合は、このクラスから切り離した方が良いです
# 規格の切り替えはこの辺で行ってます
# see https://github.com/astropy/astropy/blob/main/astropy/constants/config.py
class JasmineConstant(Constant):
    default_reference = "JASMINE"
    _registry = {}
    _has_incompatible_units = set()

class Parameters2:
    __instance = None
    __ignore_list = (
        '__is_dirty',
        '__check_dirty',
        '__constants',
        '__load_file',
        'ready',
        'apply'
    )
    def __new__(cls, *args, **kwargs):
        if Parameters2.__instance is None:
            return super(Parameters2, cls).__new__(cls)
        return Parameters2.__instance

    def __init__(self):
        if not Parameters2.__instance is None:
            return
        self.__is_dirty = True
        self.__constants = {}
        filename = pkg_resources.resource_filename('jasmine_toolkit', 'utils/constants/constants.yaml')
        self.__load_file(filename, True)
#        print(self.__constants)
        Parameters2.__instance = self

    def __setattr__(self, name, value):
        if not name.endswith(Parameters2.__ignore_list):
            self.__check_dirty(False)
            if name in self.__constants:
                self.__constants[name] = value
                return
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
#        print(name)
        if not name.endswith(Parameters2.__ignore_list):
            self.__check_dirty(True)
            if name in self.__constants:
                return self.__constants[name]
        return object.__getattribute__(self, name)

    def is_dirty(self):
        return self.__is_dirty

    def ready(self):
        self.__is_dirty = False

    def apply(self, filename):
        self.__load_file(filename, False)

    def __load_file(self, filename, init):
        with codecs.open(filename, encoding='utf-8') as file:
            obj = yaml.safe_load(file)
#            print(obj)
            for name, val in obj.items():
                if init or name in self.__constants:
                    v = _translate_value(name, val)
                    self.__constants[name] = v
                else:
                    raise AttributeError(f"'{__class__}' object has no attribute '{name}'")

    def __check_dirty(self, check):
        if self.__is_dirty == check:
            if check :
                raise RuntimeError('getter don\'t call!!')
            else:
                raise RuntimeError('setter don\'t call!!')


def _translate_value(key, dic):
    description = _extract_description(dic)
    description = description if not description == '' else key
    unit = _extract_unit(dic)
    value = _extract_value(dic)
    if type(value) == float or type(value) == int:
        #TODO uncertainty support.
        return JasmineConstant(key, description, value, unit, 0.0)
    return value


def _extract_description(dic):
    return __extract_value(dic, 'description')


def _extract_unit(dic):
    return __extract_value(dic, 'unit')


def _extract_value(dic):
    val = __extract_value(dic, 'value')
    if type(val) is bool:
        return val
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    try:
        v = eval(val)
#        print(v)
#        print(type(v))
        return v
    except BaseException:
        return val


def __extract_value(dic, key):
    return dic[key] if key in dic else ''


Parameters2()   # Python 3.7以降なら__new__自体がスレッドセーフなのでいらないらしいです
