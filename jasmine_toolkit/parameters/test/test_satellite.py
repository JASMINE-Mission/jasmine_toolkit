#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the satellite paraemters '''

import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.exception import *

from jasmine_toolkit.parameters.satellite import __all__ as all_parameters


def test_evaluate_parameters():
    for name in all_parameters:
        getattr(p.satellite, name)
