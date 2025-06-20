#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the JASMINE class in the optics module '''

import astropy.units as u
import numpy as np
from pytest import approx

from jasmine_toolkit.optics.telescope import JASMINE
from jasmine_toolkit.optics.wfe import WFEfringe37


def test_default_constructor():
    ''' Test JASMINE constructor with default parameters '''
    j = JASMINE()

    # Check default values
    assert j.xan.value == approx(0.0)
    assert j.yan.value == approx(0.0)
    assert j.defocus.value == approx(0.0)
    assert j._fovsize == 41
    assert j._simsize == 1024
    assert j._fft_oversample == 4
    assert j._detector_oversample == 4
    assert j.name == 'JASMINE'

    # Check that wfe is created when None is passed
    assert j.wfe is not None
    assert j.optsys is not None


def test_custom_angles():
    ''' Test JASMINE constructor with custom xan and yan values '''
    xan_val = 1.5 * u.deg
    yan_val = -0.8 * u.deg

    j = JASMINE(xan=xan_val, yan=yan_val)

    assert j.xan.value == approx(xan_val.value)
    assert j.yan.value == approx(yan_val.value)
    assert j.defocus.value == approx(0.0)


def test_custom_defocus():
    ''' Test JASMINE constructor with custom defocus value '''
    defocus_val = 2.5 * u.mm

    j = JASMINE(defocus=defocus_val)

    assert j.xan.value == approx(0.0)
    assert j.yan.value == approx(0.0)
    assert j.defocus.value == approx(defocus_val.value)


def test_custom_simulation_parameters():
    ''' Test JASMINE constructor with custom simulation parameters '''
    j = JASMINE(
        fovsize=51,
        simsize=2048,
        fft_oversample=8,
        detector_oversample=2
    )

    assert j._fovsize == 51
    assert j._simsize == 2048
    assert j._fft_oversample == 8
    assert j._detector_oversample == 2


def test_with_wfe_fringe37_object():
    ''' Test JASMINE constructor with a WFEfringe37 object '''
    # Create a WFEfringe37 object with specific angles
    wfe_xan = 2.0 * u.deg
    wfe_yan = 1.0 * u.deg

    wfe_obj = WFEfringe37(
        name='test_wfe',
        fringe_coeff=np.zeros(37),
        xan=wfe_xan,
        yan=wfe_yan,
        wavelength=1.0 * u.um,
        radius=1.0 * u.m
    )

    # Constructor should use angles from WFEfringe37 object
    j = JASMINE(
        xan=0.5 * u.deg,  # These should be overridden
        yan=0.3 * u.deg,  # by the WFEfringe37 object
        wfe=wfe_obj
    )

    assert j.xan.value == approx(wfe_xan.value)
    assert j.yan.value == approx(wfe_yan.value)
    assert j.wfe is wfe_obj


def test_none_angles_fallback():
    ''' Test JASMINE constructor with None angles '''
    j = JASMINE(xan=None, yan=None)

    # Should fallback to default 0.0 degrees
    assert j.xan.value == approx(0.0)
    assert j.yan.value == approx(0.0)


def test_mixed_parameter_types():
    ''' Test JASMINE constructor with mixed parameter types '''
    j = JASMINE(
        xan=1.0 * u.deg,
        yan=-0.5 * u.deg,
        defocus=1.2 * u.mm,
        fovsize=35,
        simsize=512,
        fft_oversample=2,
        detector_oversample=8
    )

    assert j.xan.value == approx(1.0)
    assert j.yan.value == approx(-0.5)
    assert j.defocus.value == approx(1.2)
    assert j._fovsize == 35
    assert j._simsize == 512
    assert j._fft_oversample == 2
    assert j._detector_oversample == 8


def test_optical_system_creation():
    ''' Test that optical system is properly created during init '''
    j = JASMINE()

    # Should have an optical system created
    assert hasattr(j, 'optsys')
    assert j.optsys is not None

    # Should be a poppy OpticalSystem
    import poppy
    assert isinstance(j.optsys, poppy.OpticalSystem)


def test_wfe_default_creation():
    ''' Test that WFE is created with correct angles when None is passed '''
    xan_val = 1.2 * u.deg
    yan_val = 0.7 * u.deg

    j = JASMINE(xan=xan_val, yan=yan_val, wfe=None)

    # WFE should be created with the provided angles
    assert j.wfe is not None
    assert hasattr(j.wfe, 'xan')
    assert hasattr(j.wfe, 'yan')
