#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' File description '''

import functools

__all__ = [
    'calculated',
    '_get_calculated_attributes',
]

__registry = {}


def calculated(func):
    ''' Decorator to register a function in the registry '''
    __registry[func.__name__] = func
    return func


def _get_calculated_attributes():
    ''' Retrieve the registered attributes '''
    return __registry
