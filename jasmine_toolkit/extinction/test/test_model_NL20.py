#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for NL20 extinction model '''

import pytest
import astropy.units as u
import numpy as np

from jasmine_toolkit.extinction.model_NL20 import NL20


@pytest.fixture
def model():
    return NL20()


def test_constructor_with_parameters():
    model = NL20(Rv=1.0, pp=0.5)
    assert isinstance(model, NL20)


def test_properties(model):
    assert model.Rv == 3.1
    assert model.pp == -0.5


def test_extinction_null(model):
    ext = model.extinction(1.0 * u.um, 0)
    assert ext.value == pytest.approx(0.0)


def test_extinction_anchor(model):
    ext = model.extinction(5500 * u.angstrom, 10.0)
    assert ext.value == pytest.approx(10.0, abs=0.1)
