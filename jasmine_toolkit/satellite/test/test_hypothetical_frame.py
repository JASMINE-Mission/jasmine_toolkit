#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for HypotheticalFrame '''

from astropy.coordinates import SkyCoord
from astropy.coordinates import CartesianRepresentation
from astropy.time import Time
import pytest
import astropy.units as u
import numpy as np

from jasmine_toolkit.satellite import HypotheticalFrame

from . import t0, tarr, p, v, galcen, grid


@pytest.fixture
def frame(t0, p, v):
    return HypotheticalFrame(obstime=t0, obsbaryloc=p, obsbaryvel=v)


def test_generate_with_t(t0):
    HypotheticalFrame(obstime=t0)


def test_generate_with_tp(t0, p):
    HypotheticalFrame(obstime=t0, obsbaryloc=p)


def test_generate_with_tv(t0, v):
    HypotheticalFrame(obstime=t0, obsbaryvel=v)


def test_generate_with_tpv(t0, p, v):
    HypotheticalFrame(obstime=t0, obsbaryloc=p, obsbaryvel=v)


def test_generate_with_tarray(tarr, p, v):
    HypotheticalFrame(obstime=tarr, obsbaryloc=p, obsbaryvel=v)


def test_attributes(frame):
    assert isinstance(frame.obstime, Time)
    assert isinstance(frame.obsbaryloc, CartesianRepresentation)
    assert isinstance(frame.obsbaryvel, CartesianRepresentation)
    assert isinstance(frame.obsgeoloc, CartesianRepresentation)
    assert isinstance(frame.obsgeovel, CartesianRepresentation)


def test_observe(frame, grid):
    frame.observe(grid)
