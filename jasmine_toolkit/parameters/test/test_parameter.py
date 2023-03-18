#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.parameter import ParameterProtected


def test_equivalency():
    assert p.naxis1 == p.detector.naxis1


def test_naxis1():
    assert p.naxis1 == 1200 * u.pix


def test_pixel_scale():
    assert p.pixel_scale == 10 * u.um


def test_assign():
    with pytest.raises(ParameterProtected):
        p.naxis1 = 10
