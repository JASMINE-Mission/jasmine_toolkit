#!/usr/bin/env python
''' JASMINE Parameter Module

Fill in a nice introduction of the module here.
'''
import sys
from .calclated_registry import _get_calculated_attributes
from .parameter import Parameter, setup_parameters
from . import detector as detector
from . import telescope as telescope

from icecream import ic


__Module = type(sys.modules['jasmine_toolkit.parameters'])


def print_parameters():
    for p in Parameter.all_parameters().values():
        print(p.info)


class ProtectedModule(__Module):
    @property
    def __calc_dict__(self):
        return _get_calculated_attributes()

    def __getattr__(self, attr):
        calculated_attr = _get_calculated_attributes()
        if attr in calculated_attr:
            return calculated_attr[attr]()
        else:
            return super()._getattr__(attr)

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super().__setattr__(attr, val)
        elif attr in self.__calc_dict__:
            raise NameError(
                f'Calculated parameter "{attr}" cannot be modified.')
        else:
            exists = getattr(self, attr, None)
            if exists is None:
                if attr == 'test':
                    super().__setattr__(attr, val)
                else:
                    raise NameError(f'"{attr}" is not defined.')
            if exists.is_compatible(val):
                if isinstance(val, Parameter):
                    super().__setattr__(attr, val)
                else:
                    reference = 'manually updated'
                    param = Parameter(
                        name=exists.name,
                        value=val,
                        unit=exists.unit,
                        description=exists.description,
                        reference=reference)
                    super().__setattr__(attr, param)
            else:
                super().__setattr__(attr, val)

for __name in sys.modules.keys():
    if __name.startswith('jasmine_toolkit.parameters'):
        sys.modules[__name].__class__ = ProtectedModule

del __name
