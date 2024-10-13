#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import astropy.units as u
import jasmine_toolkit.parameters as p
from jasmine_toolkit.parameters.exception import *


def test_equivalency():
    assert p.naxis1 == p.detector.naxis1


def test_assign_protected():
    with pytest.raises(Exception) as e:
        p.naxis1 = 10
    assert isinstance(e.value, ParameterProtected)


def test_assign_quantity():
    p.naxis1 = 1200 * u.pixel
    assert p.naxis1 == 1200 * u.pixel


def test_evaluate_before_finalized():
    with pytest.raises(Exception) as e:
        print(p.naxis1 * 10)
    assert isinstance(e.value, ParameterNotFinalized)


def test_update_parameter_quantity():
    new_naxis1 = 1100 * u.pixel
    p.naxis1.update(new_naxis1)
    assert p.naxis1 == new_naxis1


def test_update_parameter_with_unit():
    new_naxis1 = 1300
    p.naxis1.update(new_naxis1, unit=u.pixel)
    assert p.naxis1 == new_naxis1 * u.pixel


def test_update_after_finalized():
    with p.finalized_context():
        with pytest.raises(Exception) as e:
            p.naxis1.update(1200 * u.pixel)
        assert isinstance(e.value, ParameterFinalized)

        with pytest.raises(Exception) as e:
            p.naxis1.update(1200, unit=u.pixel)
        assert isinstance(e.value, ParameterFinalized)


def test_evaluate_after_finalized():
    with p.finalized_context():
        print(p.naxis1 * 10)
