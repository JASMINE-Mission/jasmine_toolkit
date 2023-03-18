#!/usr/bin/env python
import sys
from .parameter import Parameter, finalize_parameters
from .detector import *
from .telescope import *

module = sys.modules['jasmine_toolkit.parameters']
Module = type(module)


class ProtectedModule(Module):
    def __setattr__(self, attr, val):
        exists = getattr(self, attr, None)
        if exists is None:
            if attr == 'test':
                super().__setattr__(attr, val)
            else:
                raise NameError(f'"{attr}" is not defined.')
        if hasattr(exists, '__assign__'):
            exists.__assign__(val)
        super().__setattr__(attr, val)


for name in sys.modules.keys():
    if name.startswith('jasmine_toolkit.parameters'):
        module = sys.modules[name]
        module.__class__ = ProtectedModule
