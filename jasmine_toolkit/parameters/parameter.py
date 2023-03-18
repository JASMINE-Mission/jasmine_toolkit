#!/usr/bin/env python
from astropy.units.core import Unit, dimensionless_unscaled
from astropy.units.quantity import Quantity
from threading import Event, Lock
import functools
import numpy as np

__all__ = (
    'Parameter',
    'fix_parameters',
)


__parameter_fixed = Event()


class ParameterProtected(RuntimeError):
    pass


class ParameterNotFixed(RuntimeError):
    pass


class ParameterDuplicated(RuntimeError):
    pass


class ParameterUnitInconsistency(ValueError):
    pass


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
            raise ParameterNotFixed('parameter is not fixed yet.')
    return wrap


class Singleton:
    __instance = None
    __lock = Lock()

    def __new__(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.instance = super().__new__(cls)
        return cls.__instance


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


class Parameter(Quantity, Singleton, metaclass=ParameterMeta):
    __registry = {}

    def __new__(cls, name, value, unit, reference):
        name_lower = name.lower()

        inst = np.array(value, dtype=np.float64).view(cls)
        inst._name = name
        inst._value = value
        inst._unit_string = unit
        inst._reference = reference

        if name_lower in cls.__registry.keys():
            raise ParameterDuplicated(f'parameter {name} already defined')
        cls.__registry.update({name_lower: inst})

        return inst

    @classmethod
    def all_parameters(cls):
        return cls.__registry.copy()

    @classmethod
    def list_parameters(cls):
        for k, p in cls.all_parameters():
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
        raise ParameterProtected(f'Parameter {self.name} is protected.')

    def __quantity_subclass__(self, unit):
        return super().__quantity_subclass__(unit)[0], False

    def copy(self):
        '''
        Return a copy of this `Constant` instance.  Since they are by
        definition immutable, this merely returns another reference to
        ``self``.
        '''
        return self

    __deepcopy__ = __copy__ = copy

    def update(self, value, unit=None, reference=None):
        unit = unit or dimensionless_unscaled
        reference = reference or 'manually updated'

        if isinstance(value, Quantity):
            if not value.unit.is_equivalent(self.unit):
                raise ParameterUnitInconsistency('not compatible')
            self.data = np.array(value.value, dtype=np.float64).data
            self._unit_string = value.unit.to_string()
        else:
            if not Unit(unit).is_equivalent(self.unit):
                raise ParameterUnitInconsistency('not compatible')
            self.data = np.array(value, dtype=np.float64).data
            self._unit_string = unit
        self._reference = reference or 'manually defined'
        print(self.unit)

    @property
    def name(self):
        '''The full name of the constant.'''
        return self._name

    @property
    def _unit(self):
        '''The unit(s) in which this constant is defined.'''
        return Unit(self._unit_string)

    @property
    def reference(self):
        '''The source used for the value of this constant.'''
        return self._reference
