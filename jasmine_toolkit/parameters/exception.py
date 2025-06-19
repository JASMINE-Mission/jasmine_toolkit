#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Exceptions of the parameters module '''


__all__ = [
    'ParameterChanged',
    'ParameterProtected',
    'ParameterFinalized',
    'ParameterNotFinalized',
    'ParameterDuplicated',
    'UnitIncompatibleError',
]


class ParameterChanged(UserWarning):
    pass


class ParameterProtected(UserWarning):
    pass


class ParameterFinalized(UserWarning):
    pass


class ParameterNotFinalized(UserWarning):
    pass


class ParameterDuplicated(RuntimeError):
    pass


class UnitIncompatibleError(ValueError):
    pass
