#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' File description '''

import functools, inspect

__all__ = [
    'calculated',
    '_get_calculated_attributes',
]

__registry = {}


def calculated(func):
    ''' Decorator to register a function in the registry '''
    module = inspect.getmodule(inspect.stack()[1].frame)
    module_name = module.__name__
    if module_name not in __registry.keys():
        __registry[module_name] = {}
    __registry[module_name][func.__name__] = func
    return func


def _get_calculated_attributes(name):
    ''' Retrieve the registered attributes '''
    return __registry.get(name, {})
