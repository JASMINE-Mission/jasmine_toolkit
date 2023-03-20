#!/usr/bin/env python
import sys
from .parameter import *
from .detector import *
from .telescope import *

__module = sys.modules['jasmine_toolkit.parameters']
__Module = type(__module)


def print_parameters():
    for k, p in Parameter.all_parameters().items():
        print(f'# {k} ###')
        print(p)


class ProtectedModule(__Module):
    def __setattr__(self, attr, val):
        exists = getattr(self, attr, None)
        if exists is None:
            if attr == 'test':
                super().__setattr__(attr, val)
            else:
                raise NameError(f'"{attr}" is not defined.')
        if hasattr(exists, '__assign__'):
            exists.__assign__(val)
        else:
            super().__setattr__(attr, val)


for __name in sys.modules.keys():
    if __name.startswith('jasmine_toolkit.parameters'):
        __module = sys.modules[__name]
        __module.__class__ = ProtectedModule

del __name, __module, __Module
