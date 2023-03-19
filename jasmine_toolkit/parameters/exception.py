#!/usr/bin/env python

__all__ = (
    'ParameterProtected',
    'ParameterFinalized',
    'ParameterNotFinalized',
    'ParameterDuplicated',
    'UnitIncompatibility',
)


class ParameterProtected(RuntimeError):
    pass


class ParameterFinalized(RuntimeError):
    pass


class ParameterNotFinalized(RuntimeError):
    pass


class ParameterDuplicated(RuntimeError):
    pass


class UnitIncompatibility(ValueError):
    pass
