#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the pupil module '''

import astropy.units as u
import poppy

from jasmine_toolkit.optics.pupil import get_pupil, get_obscuration
import jasmine_toolkit.parameters.telescope as tel


def test_get_pupil_default_parameters():
    ''' Test get_pupil with default parameters '''

    pupil = get_pupil()

    # Should return a CompoundAnalyticOptic
    assert isinstance(pupil, poppy.CompoundAnalyticOptic)

    # Should have 4 components: WFE, pupil, obscuration, defocus
    assert len(pupil.opticslist) == 4

    # Check default name
    assert pupil.name == 'entrance pupil'


def test_get_pupil_custom_name():
    ''' Test get_pupil with custom name '''

    custom_name = 'test pupil'
    pupil = get_pupil(name=custom_name)

    assert pupil.name == custom_name


def test_get_pupil_with_custom_angles():
    ''' Test get_pupil with custom xan and yan angles '''

    xan = 0.1 * u.deg
    yan = 0.2 * u.deg

    pupil = get_pupil(xan=xan, yan=yan)

    # Should still return a valid CompoundAnalyticOptic
    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_custom_defocus():
    ''' Test get_pupil with custom defocus offset '''

    defocus = 1.0 * u.mm

    pupil = get_pupil(defocus=defocus)

    # Should still return a valid CompoundAnalyticOptic
    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_custom_primary_radius():
    ''' Test get_pupil with custom primary radius '''

    primary_radius = 0.5 * u.m

    pupil = get_pupil(primary_radius=primary_radius)

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_custom_secondary_parameters():
    ''' Test get_pupil with custom secondary mirror parameters '''

    secondary_radius = 0.1 * u.m
    pupil_to_m2_distance = 2.0 * u.m
    obscuration_depth = 0.05 * u.m

    pupil = get_pupil(
        secondary_radius=secondary_radius,
        pupil_to_m2_distance=pupil_to_m2_distance,
        obscuration_depth=obscuration_depth
    )

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_custom_support_parameters():
    ''' Test get_pupil with custom support strut parameters '''

    n_supports = 6
    support_width = 0.02 * u.m
    support_angle_offset = 30.0 * u.deg

    pupil = get_pupil(
        n_supports=n_supports,
        support_width=support_width,
        support_angle_offset=support_angle_offset
    )

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_custom_wavelength():
    ''' Test get_pupil with custom reference wavelength '''

    reference_wavelength = 1000.0 * u.nm

    pupil = get_pupil(reference_wavelength=reference_wavelength)

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_with_zernike_wfe():
    ''' Test get_pupil with custom ZernikeWFE '''

    # Create a simple ZernikeWFE
    wfe = poppy.ZernikeWFE(
        coefficients=[0, 0, 0, 100e-9],  # 100 nm of defocus
        radius=tel.pupil_radius
    )

    pupil = get_pupil(wfe=wfe)

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4

    # First plane should be the provided WFE
    assert pupil.opticslist[0] is wfe


def test_get_pupil_with_wfe_fringe37():
    ''' Test get_pupil with WFEfringe37 instance '''

    # Create a WFEfringe37 instance
    from jasmine_toolkit.optics.wfe import get_wfe_fringe37
    wfe_fringe = get_wfe_fringe37(
        xan=0.0 * u.deg,
        yan=0.0 * u.deg,
        primary_radius=tel.pupil_radius
    )

    pupil = get_pupil(wfe=wfe_fringe)

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4


def test_get_pupil_all_custom_parameters():
    ''' Test get_pupil with all custom parameters '''

    pupil = get_pupil(
        name='test_pupil',
        xan=0.05 * u.deg,
        yan=0.1 * u.deg,
        defocus=0.5 * u.mm,
        primary_radius=0.6 * u.m,
        pupil_to_m2_distance=1.8 * u.m,
        obscuration_depth=0.03 * u.m,
        secondary_radius=0.08 * u.m,
        n_supports=4,
        support_width=0.015 * u.m,
        support_angle_offset=45.0 * u.deg,
        reference_wavelength=800.0 * u.nm
    )

    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
    assert len(pupil.opticslist) == 4
    assert pupil.name == 'test_pupil'


def test_get_obscuration_function():
    ''' Test the get_obscuration function separately '''

    xan = 0.1 * u.deg
    yan = 0.2 * u.deg
    secondary_radius = 0.1 * u.m
    pupil_to_m2_distance = 2.0 * u.m
    obscuration_depth = 0.05 * u.m
    n_supports = 4
    support_width = 0.02 * u.m
    support_angle_offset = 45.0 * u.deg

    obscuration = get_obscuration(
        xan=xan,
        yan=yan,
        secondary_radius=secondary_radius,
        pupil_to_m2_distance=pupil_to_m2_distance,
        obscuration_depth=obscuration_depth,
        n_supports=n_supports,
        support_width=support_width,
        support_angle_offset=support_angle_offset
    )

    # Should return a CompoundAnalyticOptic with 2 layers
    assert isinstance(obscuration, poppy.CompoundAnalyticOptic)
    assert len(obscuration.opticslist) == 2
    assert obscuration.name == 'JASMINE obscuration'


def test_get_pupil_error_handling():
    ''' Test get_pupil error handling with invalid inputs '''

    # These should not raise errors, but handle gracefully
    # Test with very small radius
    pupil = get_pupil(primary_radius=0.001 * u.m)
    assert isinstance(pupil, poppy.CompoundAnalyticOptic)

    # Test with very large angles (within reasonable bounds)
    pupil = get_pupil(xan=1.0 * u.deg, yan=1.0 * u.deg)
    assert isinstance(pupil, poppy.CompoundAnalyticOptic)
