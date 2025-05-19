#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the WFEfringe37 class. '''

from ..wfe import WFEfringe37
from ..zernike import noll_normalize

import pytest
import poppy
import astropy.units as u


@pytest.fixture
def fringe_coeff():
    return [
        0.1 * noll_normalize(0,  0, False),
        0.2 * noll_normalize(1,  1, False),
        0.3 * noll_normalize(1, -1, False),
        0.4 * noll_normalize(2,  0, False),
        0.5 * noll_normalize(2,  2, False),
        0.6 * noll_normalize(2, -2, False),
        0.7 * noll_normalize(3,  1, False),
        0.8 * noll_normalize(3, -1, False),
        0.9 * noll_normalize(4,  0, False),
    ]


def test_wavefront_error_init():
    ''' Test the initialization of the WFEfringe37 class. '''
    wfe = WFEfringe37(
        name='Test WFE',
        fringe_coeff=[0.1, 0.2, 0.3],
        xan=0.5,
        yan=0.5,
        wavelength=5500 * u.angstrom,
        radius=0.5 * u.m
    )

    assert wfe.name == 'Test WFE'
    assert wfe.fringe_coeff == [0.1, 0.2, 0.3]
    assert wfe.xan == 0.5
    assert wfe.yan == 0.5
    assert wfe.wavelength == 5500 * u.angstrom
    assert wfe.radius == 0.5 * u.m


def test_wavefront_error_coeff(fringe_coeff):
    ''' Test the conversion of fringe coefficients to Noll coefficients. '''
    wfe = WFEfringe37(
        name='Test WFE',
        fringe_coeff=fringe_coeff,
        xan=0.5,
        yan=0.5,
        wavelength=5500 * u.angstrom,
        radius=0.5 * u.m
    )

    assert wfe.coeff.shape == (79, )

    # Assuming convert_fringe37_to_noll is implemented correctly
    expected_coeff = [
      0.0, 0.0, 0.0, 0.4, 0.6, 0.5, 0.8, 0.7, 0.0, 0.0, 0.9]
    assert wfe.coeff[:11] == pytest.approx(expected_coeff)


def test_wavefront_error_coeff_no_centering(fringe_coeff):
    ''' Test the conversion of fringe coefficients to Noll coefficients. '''
    wfe = WFEfringe37(
        name='Test WFE',
        fringe_coeff=fringe_coeff,
        xan=0.5,
        yan=0.5,
        wavelength=5500 * u.angstrom,
        radius=0.5 * u.m,
        centering=False
    )

    assert wfe.coeff.shape == (79, )

    # Assuming convert_fringe37_to_noll is implemented correctly
    expected_coeff = [
      0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.8, 0.7, 0.0, 0.0, 0.9]
    assert wfe.coeff[:11] == pytest.approx(expected_coeff)


def test_wavefront_error_generate_wfe(fringe_coeff):
    ''' Test the generation of the poppy.ZernikeWFE object. '''
    wfe = WFEfringe37(
        name='Test WFE',
        fringe_coeff=fringe_coeff,
        xan=0.5,
        yan=0.5,
        wavelength=5500 * u.angstrom,
        radius=0.5 * u.m
    )

    assert isinstance(wfe.wfe, poppy.ZernikeWFE)
