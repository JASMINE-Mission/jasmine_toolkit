#!/usr/bin/env python
from astropy.units.core import Unit
from astropy.units.quantity import Quantity
from astropy.utils import lazyproperty
from threading import Event
import functools
import numpy as np

__all__ = (
    'Parameter',
    'fix_parameters',
)


__parameter_fixed = Event()


def fix_parameters():
    __parameter_fixed.set()


def not_dirty(func):
    @functools.wraps(func)
    def wrap(*args, **params):
        print('dirty check start')
        print(__parameter_fixed)
        if __parameter_fixed.is_set():
            return func(*args, **params)
        else:
            raise Exception('parameter is not fixed yet.')
    return wrap


class ParameterMeta(type):
    def __new__(mcls, name, bases, d):
        protected = [
            '_to_value',
            '__mul__',
            '__div__',
            '__add__',
            '__sub__',
        ]
        for attr, value in vars(Quantity).items():
            if attr in protected:
                d[attr] = not_dirty(value)
        return super().__new__(mcls, name, bases, d)


class Parameter(Quantity, metaclass=ParameterMeta):
    __registry = {}

    def __new__(cls, name, value, unit, reference):
        name_lower = name.lower()

        inst = np.array(value).view(cls)
        inst._name = name
        inst._value = value
        inst._unit_string = unit
        inst._reference = reference

        if name_lower in cls.__registry.keys():
            raise Exception(f'parameter {name} already defined')
        cls.__registry.update({name_lower: inst})

        return inst

    @classmethod
    def list_parameters(cls):
        for k, p in cls.__registry.items():
            print(f'### {k}')
            print(p)

    def __repr__(self):
        return (
            f'<{self.__class__} '
            f'name={self.name!r} '
            f'value={self.value} '
            f'unit={str(self.unit)!r} '
            f'reference={self.reference!r}>'
        )

    def __str__(self):
        return (
            f'  Name   = {self.name}\n'
            f'  Value  = {self.value}\n'
            f'  Unit  = {self.unit}\n'
            f'  Reference = {self.reference}'
        )

    def __assign__(self, value):
        raise Exception(f'Assigning to {self.name} is not allowed.')

    def __quantity_subclass__(self, unit):
        return super().__quantity_subclass__(unit)[0], False

    def copy(self):
        """
        Return a copy of this `Constant` instance.  Since they are by
        definition immutable, this merely returns another reference to
        ``self``.
        """
        return self

    __deepcopy__ = __copy__ = copy

    @property
    def name(self):
        '''The full name of the constant.'''
        return self._name

    @lazyproperty
    def _unit(self):
        '''The unit(s) in which this constant is defined.'''
        return Unit(self._unit_string)

    @property
    def reference(self):
        '''The source used for the value of this constant.'''
        return self._reference
