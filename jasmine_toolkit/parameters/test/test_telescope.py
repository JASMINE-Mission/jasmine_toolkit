#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the telescope parameters '''

import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.exception import *

from jasmine_toolkit.parameters.telescope import __all__ as all_parameters


def test_evaluate_parameters():
    for name in all_parameters:
        getattr(p.telescope, name)


def test_effective_focal_length():
    efl  = p.telescope.effective_focal_length.quantity
    diameter = p.telescope.pupil_diameter.quantity
    f_number = p.telescope.f_number.quantity
    assert efl == diameter * f_number

    print(f_number, type(f_number))
    with p.update_parameters():
        p.telescope.f_number = f_number * 2

    diff = efl - p.telescope.effective_focal_length / 2.0
    assert diff.value == pytest.approx(0)
