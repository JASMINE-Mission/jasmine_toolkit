#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.exception import *


def test_assign_incompatible():
    with pytest.raises(Exception) as e:
        p.detector.naxis1 = 10
    assert isinstance(e.value, TypeError)

    with pytest.raises(Exception) as e:
        p.detector.naxis1 = 10 * u.m
    assert isinstance(e.value, UnitIncompatibleError)


def test_assign_quantity():
    p.detector.naxis1 = 1200 * u.pixel
    assert isinstance(p.detector.naxis1, p.Parameter)
    assert p.detector.naxis1 == 1200 * u.pixel


def test_evaluate_before_finalized():
    with p.setup_parameters():
        print(p.detector.naxis1 * 10)


def test_update_parameter_quantity():
    new_naxis1 = 1100 * u.pixel
    p.detector.naxis1 = new_naxis1
    assert p.detector.naxis1 == new_naxis1


def test_update_parameter_with_unit():
    new_naxis1 = 1300 * u.pixel
    p.detector.naxis1 = p.detector.naxis1.updated(new_naxis1)
    assert p.detector.naxis1 == new_naxis1
