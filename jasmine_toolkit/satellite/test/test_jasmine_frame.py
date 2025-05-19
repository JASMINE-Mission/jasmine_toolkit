#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for JASMINEFrame '''

from astropy.coordinates import SkyCoord
from astropy.coordinates import CartesianRepresentation
from astropy.time import Time
import pytest
import astropy.units as u
import numpy as np

from jasmine_toolkit.satellite import JASMINEFrame

from . import t0, tarr, galcen, grid


@pytest.fixture
def frame(tarr):
    return JASMINEFrame(obstime=tarr)


def test_generate_with_t(t0):
    JASMINEFrame(obstime=t0)


def test_generate_with_tarr(tarr):
    JASMINEFrame(obstime=tarr)


def test_generate_with_phase(tarr):
    JASMINEFrame(obstime=tarr, phase=0.0)


def test_generate_with_altitude(tarr):
    JASMINEFrame(obstime=tarr, altitude=3.6e4*u.km)


def test_phase_update(frame):
    frame.with_updated_phase()


def test_velocity_error(frame):
    other = frame.with_velocity_error(0.0 * u.m / u.s)
    dv = other.obsgeovel - frame.obsgeovel
    assert dv.xyz.std().value < 1e-9

    other = frame.with_velocity_error(1.0 * u.m / u.s)
    dv = other.obsgeovel - frame.obsgeovel
    assert dv.xyz.std().value > 1e-9


def test_attributes(frame):
    assert isinstance(frame.obstime, Time)
    assert isinstance(frame.obsbaryloc, CartesianRepresentation)
    assert isinstance(frame.obsbaryvel, CartesianRepresentation)
    assert isinstance(frame.obsgeoloc, CartesianRepresentation)
    assert isinstance(frame.obsgeovel, CartesianRepresentation)


def test_jasmine_spec(frame):
    assert frame.plate_scale is not None
    assert frame.pixel_scale is not None
    assert frame.orbital_radius is not None
    assert frame.orbital_velocity is not None
    assert frame.orbital_period is not None
    assert frame.nadir_horizon_angle is not None
    assert frame.sun_direction is not None
    assert frame.ecliptic_longitude is not None


def test_wcs_object(frame, galcen):
    wcs0 = frame.wcs(galcen.ra, galcen.dec)
    wcs1 = frame.wcs(galcen.ra, galcen.dec, 90 * u.deg)
    assert wcs0 is not None
    assert wcs0 != wcs1


def test_earth_separation(frame, galcen, grid):
    frame.earth_separation(galcen)
    frame.earth_separation(grid)


def test_earth_avoidance(frame, galcen, grid):
    frame.earth_avoidance(galcen)
    frame.earth_avoidance(grid)


def test_solar_separation(frame, galcen, grid):
    frame.solar_separation(galcen)
    frame.solar_separation(grid)


def test_observable(frame, galcen, grid):
    frame.observable(galcen)
    frame.observable(grid)


def test_observe(frame, grid):
    frame[0].observe(grid)
