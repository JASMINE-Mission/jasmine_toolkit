import threading

class Parameters2:
    __instance = None
    __ignore_list = (
        '__is_dirty',
        '__check_dirty'
    )
    def __new__(cls, *args, **kwargs):
        if Parameters2.__instance is None:
            Parameters2.__instance = super(Parameters2, cls).__new__(cls)
        return Parameters2.__instance

    def __init__(self):
        self.__is_dirty = True
        self.__dummy = 123

    def __setattr__(self, name, value):
        if not name.endswith(Parameters2.__ignore_list):
            self.__check_dirty(False)
        object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        if not name.endswith(Parameters2.__ignore_list):
            self.__check_dirty(True)
        return object.__getattribute__(self, name)

    @property
    def dummy(self):
        return self.__dummy

    @dummy.setter
    def dummy(self, dummy):
        self.__dummy = dummy

    def is_dirty(self):
        return self.__is_dirty

    def ready(self):
        self.__is_dirty = False

    def __check_dirty(self, check):
        if self.__is_dirty == check:
            if check :
                raise RuntimeError('getter don\'t call!!')
            else:
                raise RuntimeError('setter don\'t call!!')


Parameters2()   # Python 3.7以降なら__new__自体がスレッドセーフなのでいらないらしいです