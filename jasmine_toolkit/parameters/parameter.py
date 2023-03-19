#!/usr/bin/env python
from astropy.units.core import Unit, dimensionless_unscaled
from astropy.units.quantity import Quantity
from threading import Event
from contextlib import contextmanager
import functools
import numpy as np

from .exception import *


__all__ = (
    'Parameter',
    'finalize_parameters',
    'finalized_context',
)


__parameter_finalized = Event()


def finalize_parameters():
    __parameter_finalized.set()


def unfinalize_parameters():
    __parameter_finalized.clear()


@contextmanager
def finalized_context():
    try:
        yield finalize_parameters()
    finally:
        unfinalize_parameters()


def parameter_finalized(func):
    @functools.wraps(func)
    def wrap(*args, **params):
        if __parameter_finalized.is_set():
            return func(*args, **params)
        else:
            raise ParameterNotFinalized('parameters are not finalized yet.')
    return wrap


def parameter_adjustable(func):
    @functools.wraps(func)
    def wrap(*args, **params):
        if not __parameter_finalized.is_set():
            return func(*args, **params)
        else:
            raise ParameterFinalized('parameters are already finalized.')
    return wrap


class ParameterMeta(type):
    def __new__(mcls, name, bases, d):
        protected = [
            '_to_value',
            '__add__', '__sub__',
            '__neg__', '__pos__',
            '__mul__', '__div__', '__truediv__', '__floordiv__',
            '__and__', '__or__',
        ]
        for attr, value in vars(Quantity).items():
            if attr in protected:
                d[attr] = parameter_finalized(value)
        return super().__new__(mcls, name, bases, d)


class Parameter(Quantity, metaclass=ParameterMeta):
    __registry = {}

    def __new__(cls, name, value, unit, description, reference):
        name_lower = name.lower()

        inst = np.array(value, dtype=np.float64).view(cls)
        inst._name = name
        inst._unit_string = unit
        inst._unit_string_orig = unit
        inst._description = description
        inst._reference = reference

        if name_lower in cls.__registry.keys():
            raise ParameterDuplicated(f'parameter {name} already defined')
        cls.__registry.update({name_lower: inst})

        return inst

    @classmethod
    def all_parameters(cls):
        return cls.__registry.copy()

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
            f'  Name        = {self.name}\n'
            f'  Value       = {self.value}\n'
            f'  Unit        = {self.unit}\n'
            f'  Description = {self.description}\n'
            f'  Reference   = {self.reference}'
        )

    def __quantity_subclass__(self, unit):
        return super().__quantity_subclass__(unit)[0], False

    @property
    def __all(self):
        return np.full(self.shape, True)

    @parameter_adjustable
    def __assign__(self, value):
        if isinstance(value, Quantity):
            self.update(value)
        else:
            raise ParameterProtected(f'Parameter {self.name} is protected.')

    @parameter_adjustable
    def update(self, value, unit=None, reference=None):
        unit = unit or dimensionless_unscaled
        reference = reference or 'manually updated'

        if isinstance(value, Quantity):
            if not value.unit.is_equivalent(self.unit):
                raise UnitIncompatibility('not compatible')
            np.place(self, self.__all, value.copy())
            self._unit_string = value.unit.to_string()
        else:
            if not Unit(unit).is_equivalent(self.unit):
                raise UnitIncompatibility('not compatible')
            np.place(self, self.__all, Quantity(value, unit=unit).copy())
            self._unit_string = unit
        self._reference = reference or 'manually defined'

    @property
    def name(self):
        ''' The full name of the parameter. '''
        return self._name

    @property
    def _unit(self):
        '''The unit(s) in which this parameter is defined.'''
        return Unit(self._unit_string_orig)

    @property
    def description(self):
        ''' The description of the parameter. '''
        return self._description

    @property
    def reference(self):
        ''' The source used for the value of this parameter. '''
        return self._reference

    def copy(self):
        '''
        Return a copy of this `Constant` instance.  Since they are by
        definition immutable, this merely returns another reference to
        ``self``.
        '''
        return self

    __deepcopy__ = __copy__ = copy
