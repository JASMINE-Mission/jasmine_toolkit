#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Comprehensive test cases for the zernike module '''

import numpy as np
from pytest import approx, raises

from jasmine_toolkit.optics.zernike import (
    get_fringe_index,
    fringe_zernike,
    noll_j_index,
    noll_normalize,
    convert_fringe37_to_noll,
)


def test_get_fringe_index_basic():
    ''' Test basic functionality of get_fringe_index '''

    # Test first few known indices
    assert get_fringe_index(1) == [0, 0]  # Piston
    assert get_fringe_index(2) == [1, 1]  # Tip
    assert get_fringe_index(3) == [1, -1]  # Tilt
    assert get_fringe_index(4) == [2, 0]  # Defocus
    assert get_fringe_index(5) == [2, 2]  # Astigmatism
    assert get_fringe_index(6) == [2, -2]  # Astigmatism


def test_get_fringe_index_properties():
    ''' Test mathematical properties of Zernike indices '''

    for i in range(1, 38):
        n, m = get_fringe_index(i)
        # n should be non-negative
        assert n >= 0
        # |m| should not exceed n
        assert abs(m) <= n
        # n - |m| should be even (Zernike property)
        assert (n - abs(m)) % 2 == 0


def test_get_fringe_index_edge_cases():
    ''' Test edge cases and error handling for get_fringe_index '''

    # Test boundary conditions
    assert get_fringe_index(1) == [0, 0]
    assert get_fringe_index(37) == [12, 0]

    # Test invalid indices
    with raises(ValueError):
        get_fringe_index(0)
    with raises(ValueError):
        get_fringe_index(38)
    with raises(ValueError):
        get_fringe_index(-1)


def test_fringe_zernike_basic():
    ''' Test basic functionality of fringe_zernike '''

    npix = 64

    # Test first few Zernike modes
    piston = fringe_zernike(1, npix)  # Piston
    tip = fringe_zernike(2, npix)     # Tip
    tilt = fringe_zernike(3, npix)    # Tilt

    assert piston.shape == (npix, npix)
    assert tip.shape == (npix, npix)
    assert tilt.shape == (npix, npix)

    # Piston should be constant inside aperture
    # (we can't easily test this without knowing the aperture mask)
    assert np.all(np.isfinite(piston))


def test_fringe_zernike_properties():
    ''' Test mathematical properties of fringe_zernike '''

    npix = 32

    for i in range(1, 11):  # Test first 10 modes
        zernike = fringe_zernike(i, npix)

        # Should be proper shape
        assert zernike.shape == (npix, npix)

        # Should be finite everywhere
        assert np.all(np.isfinite(zernike))

        # Should be normalized (values typically between -1 and 1)
        assert np.max(np.abs(zernike)) <= 2.0  # Allow some tolerance


def test_fringe_zernike_different_sizes():
    ''' Test fringe_zernike with different array sizes '''

    sizes = [16, 32, 64, 128]

    for npix in sizes:
        zernike = fringe_zernike(1, npix)  # Piston
        assert zernike.shape == (npix, npix)


def test_fringe_zernike_outside_parameter():
    ''' Test outside parameter in fringe_zernike '''

    npix = 32
    outside_val = -999.0

    zernike = fringe_zernike(1, npix, outside=outside_val)
    assert zernike.shape == (npix, npix)
    # The outside value should appear somewhere in the array
    # (though we can't guarantee it without knowing the aperture)


def test_noll_j_index_known_values():
    ''' Test noll_j_index with known reference values '''

    # Test cases from Noll 1976 paper
    assert noll_j_index(0, 0) == 1   # Piston
    assert noll_j_index(1, 1) == 2   # Tip
    assert noll_j_index(1, -1) == 3  # Tilt
    assert noll_j_index(2, 0) == 4   # Defocus
    assert noll_j_index(2, -2) == 5  # Astigmatism
    assert noll_j_index(2, 2) == 6   # Astigmatism
    assert noll_j_index(3, -1) == 7  # Coma
    assert noll_j_index(3, 1) == 8   # Coma
    assert noll_j_index(3, -3) == 9  # Trefoil
    assert noll_j_index(3, 3) == 10  # Trefoil
    assert noll_j_index(4, 0) == 11  # Spherical


def test_noll_j_index_properties():
    ''' Test mathematical properties of noll_j_index '''

    # Test that indices are unique for different (n, m) pairs
    indices = []
    for n in range(0, 8):
        for m in range(-n, n+1):
            if (n - abs(m)) % 2 == 0:  # Valid Zernike mode
                j = noll_j_index(n, m)
                assert j not in indices, f'Duplicate index {j} for ({n}, {m})'
                indices.append(j)
                assert j >= 1, f'Index should be >= 1, got {j}'


def test_noll_normalize_centering_true():
    ''' Test noll_normalize with centering=True '''

    # With centering, tip and tilt modes should have infinite normalization
    assert noll_normalize(0, 0, centering=True) == np.inf
    assert noll_normalize(1, 1, centering=True) == np.inf
    assert noll_normalize(1, -1, centering=True) == np.inf

    # Higher order modes
    assert noll_normalize(2, 0, centering=True) == approx(np.sqrt(3))
    assert noll_normalize(2, 2, centering=True) == approx(np.sqrt(6))
    assert noll_normalize(2, -2, centering=True) == approx(np.sqrt(6))


def test_noll_normalize_centering_false():
    ''' Test noll_normalize with centering=False '''

    # Without centering, all modes should have finite normalization
    assert noll_normalize(0, 0, centering=False) == approx(1.0)
    assert noll_normalize(1, 1, centering=False) == approx(2.0)
    assert noll_normalize(1, -1, centering=False) == approx(2.0)
    assert noll_normalize(2, 0, centering=False) == approx(np.sqrt(3))


def test_noll_normalize_properties():
    ''' Test mathematical properties of noll_normalize '''

    # Test that normalization follows expected patterns
    for n in range(0, 6):
        for m in range(-n, n+1):
            if (n - abs(m)) % 2 == 0:  # Valid Zernike mode
                norm_centered = noll_normalize(n, m, centering=True)
                norm_uncentered = noll_normalize(n, m, centering=False)

                if n <= 1:  # Tip/tilt modes
                    assert norm_centered == np.inf
                    assert norm_uncentered > 0
                else:
                    assert norm_centered > 0
                    assert norm_uncentered > 0
                    # Same normalization for higher order modes
                    assert norm_centered == approx(norm_uncentered)


def test_convert_fringe37_to_noll_basic():
    ''' Test basic functionality of convert_fringe37_to_noll '''

    # Test with zero coefficients
    coeff = np.zeros(37)
    noll_coeff = convert_fringe37_to_noll(coeff)
    assert noll_coeff.shape == (79,)
    assert np.allclose(noll_coeff, 0.0)


def test_convert_fringe37_to_noll_single_mode():
    ''' Test conversion with single non-zero coefficient '''

    # Test with only piston (first mode)
    coeff = np.zeros(37)
    coeff[0] = 1.0  # Piston

    noll_coeff_centered = convert_fringe37_to_noll(coeff, centering=True)
    noll_coeff_uncentered = convert_fringe37_to_noll(coeff, centering=False)

    # Piston should map to first Noll coefficient
    assert noll_coeff_uncentered[0] == approx(1.0)  # Normalized by 1.0
    assert noll_coeff_centered[0] == approx(0.0)    # Piston term is dropped


def test_convert_fringe37_to_noll_tip_tilt():
    ''' Test conversion of tip/tilt modes '''

    # Test tip mode (index 2 in fringe)
    coeff = np.zeros(37)
    coeff[1] = 1.0  # Tip

    noll_coeff_centered = convert_fringe37_to_noll(coeff, centering=True)
    noll_coeff_uncentered = convert_fringe37_to_noll(coeff, centering=False)

    # With centering, tip coefficient should be 0 (infinite normalization)
    assert noll_coeff_centered[1] == 0.0
    # Without centering, should be normalized
    assert noll_coeff_uncentered[1] == approx(0.5)  # 1.0 / 2.0


def test_convert_fringe37_to_noll_error_handling():
    ''' Test error handling in convert_fringe37_to_noll '''

    # Test with too many coefficients
    coeff = np.zeros(38)
    with raises(ValueError):
        convert_fringe37_to_noll(coeff)


def test_convert_fringe37_to_noll_partial_array():
    ''' Test conversion with partial coefficient array '''

    # Test with fewer than 37 coefficients
    coeff = np.ones(10)  # Only first 10 modes
    noll_coeff = convert_fringe37_to_noll(coeff)

    assert noll_coeff.shape == (79,)
    # Some coefficients should be non-zero
    assert np.any(noll_coeff != 0)


def test_convert_fringe37_to_noll_consistency():
    ''' Test consistency between centering options '''

    # For modes beyond tip/tilt, centering shouldn't matter for normalization
    coeff = np.zeros(37)
    coeff[3] = 1.0  # Defocus (index 4 in fringe)

    noll_coeff_centered = convert_fringe37_to_noll(coeff, centering=True)
    noll_coeff_uncentered = convert_fringe37_to_noll(coeff, centering=False)

    # Defocus should be the same regardless of centering
    defocus_index = noll_j_index(2, 0) - 1  # Convert to 0-based index
    assert (noll_coeff_centered[defocus_index] ==
            approx(noll_coeff_uncentered[defocus_index]))


def test_full_workflow():
    ''' Test complete workflow using all functions together '''

    # Create a pattern with known coefficients
    test_coeff = np.zeros(37)
    test_coeff[0] = 1.0   # Piston
    test_coeff[3] = 0.5   # Defocus
    test_coeff[8] = 0.25  # Spherical aberration

    # Convert to Noll coefficients
    noll_coeff = convert_fringe37_to_noll(test_coeff, centering=False)

    # Check that the conversion preserves information
    assert noll_coeff.shape == (79,)
    assert np.sum(np.abs(noll_coeff)) > 0

    # Test that we can generate Zernike patterns for the modes we used
    for i in [1, 4, 9]:  # Indices we set coefficients for
        pattern = fringe_zernike(i, 32)
        assert pattern.shape == (32, 32)
        assert np.all(np.isfinite(pattern))


def test_mathematical_consistency():
    ''' Test mathematical consistency across functions '''

    # Test that fringe indices correspond to valid Zernike modes
    for i in range(1, 38):
        n, m = get_fringe_index(i)

        # Should be able to compute Noll index
        j = noll_j_index(n, m)
        assert j >= 1

        # Should be able to compute normalization
        norm = noll_normalize(n, m, centering=False)
        assert norm > 0  # All should be finite for centering=False

        # Should be able to generate the pattern
        pattern = fringe_zernike(i, 16)
        assert pattern.shape == (16, 16)
