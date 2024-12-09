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
            p.detector.naxis1 = 10
    assert isinstance(e.value, UnitIncompatibleError)

    with pytest.raises(Exception) as e:
        with p.update_parameters():
            p.detector.naxis1 = 10 * u.m
    assert isinstance(e.value, UnitIncompatibleError)


def test_assign_compatible():
    with p.update_parameters():
        p.detector.naxis1 = 1200 * u.pixel
    assert isinstance(p.detector.naxis1, p.Parameter)
    assert p.detector.naxis1 == 1200 * u.pixel

    with p.update_parameters():
        new_naxis1 = 1100 * u.pixel
        p.detector.naxis1 = new_naxis1
    assert p.detector.naxis1 == new_naxis1

    with p.update_parameters():
        new_naxis1 = 1300 * u.pixel
        p.detector.naxis1 = p.detector.naxis1.updated(new_naxis1)
    assert p.detector.naxis1 == new_naxis1


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
