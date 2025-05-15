#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the satellite module '''

from astropy.coordinates import SkyCoord
from astropy.coordinates import CartesianRepresentation
from astropy.time import Time
import pytest
import astropy.units as u
import numpy as np

from jasmine_toolkit.distortion import generate_grid


@pytest.fixture
def galcen():
    coo = SkyCoord(0.0 * u.deg, 0.0 * u.deg, frame='galactic')
    return coo.icrs


@pytest.fixture
def grid(galcen):
    return generate_grid(galcen.ra, galcen.dec)


@pytest.fixture
def t0():
    return Time(2024.0, format='jyear', scale='tcb')


@pytest.fixture
def tarr(t0):
    return t0 + np.linspace(0, 10, 11) * u.day


@pytest.fixture
def p():
    return CartesianRepresentation(
        1.0 * u.au, 0.0 * u.au, 0.0 * u.au)


@pytest.fixture
def v():
    kms = u.km / u.s
    return CartesianRepresentation(
        1.0 * kms, 0.0 * kms, 0.0 * kms)
