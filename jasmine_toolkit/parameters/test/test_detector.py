#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the detector parameters '''

import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.exception import *

from jasmine_toolkit.parameters.detector import __all__ as all_parameters


def test_evaluate_parameters():
    for name in all_parameters:
        getattr(p.detector, name)


def test_assign_incompatible():
    with pytest.raises(Exception) as e:
        with p.update_parameters():
            p.detector.pixel_size = 10
    assert isinstance(e.value, UnitIncompatibleError)

    with pytest.raises(Exception) as e:
        with p.update_parameters():
            p.detector.pixel_size = 10 * u.s
    assert isinstance(e.value, UnitIncompatibleError)


def test_assign_compatible():
    with p.update_parameters():
        p.detector.pixel_size = 20 * u.um
    assert isinstance(p.detector.pixel_size, p.Parameter)
    assert p.detector.pixel_size == 20 * u.um

    with p.update_parameters():
        new_pixsize = 10 * u.um
        p.detector.pixel_size = new_pixsize
    assert p.detector.pixel_size == new_pixsize

    with p.update_parameters():
        new_pixsize = 30 * u.um
        p.detector.pixel_size = p.detector.pixel_size.updated(new_pixsize)
    assert p.detector.pixel_size == new_pixsize


def test_unexpected_assignment():
    with pytest.raises(Exception) as e:
        p.detector.pixel_scale = 1.0e-5 * u.degree
    assert isinstance(e.value, NameError)


def test_evaluate_before_finalized():
    with pytest.raises(Exception) as e:
        with p.update_parameters():
            print(p.detector.naxis1 * 10)
    assert isinstance(e.value, ParameterNotFinalized)


def test_pixel_scale():
    pix_scale = p.detector.pixel_scale

    with p.update_parameters():
        p.telescope.f_number = 12.14 / 2.0

    diff = pix_scale - p.detector.pixel_scale / 2.0
    assert diff.value == pytest.approx(0)
