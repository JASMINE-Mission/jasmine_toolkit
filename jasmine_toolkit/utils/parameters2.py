import threading

class Parameters2:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Parameters2.__instance is None:
            Parameters2.__instance = super(Parameters2, cls).__new__(cls)
        return Parameters2.__instance

    def __init__(self):
        self.__is_dirty = True
        self.__dummy = 123

    @property
    def dummy(self):
        self.__check_dirty(True)
        return self.__dummy

    @dummy.setter
    def dummy(self, dummy):
        self.__check_dirty(False)
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