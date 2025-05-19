#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Generating Zernike polynomial fringe patterns '''

from poppy.zernike import zernike as poppy_zernike
import numpy as np


__all__ = [
    'get_fringe_index',
    'fringe_zernike',
    'noll_j_index',
    'noll_normalize',
    'convert_fringe37_to_noll',
]


__fringe_zernike_index = (
    [0, 0],
    [1, 1], [1, -1], [2, 0],
    [2, 2], [2, -2], [3, 1], [3, -1], [4, 0],
    [3, 3], [3, -3], [4, 2], [4, -2], [5, 1], [5, -1], [6, 0],
    [4, 4], [4, -4], [5, 3], [5, -3],
        [6, 2], [6, -2], [7, 1], [7, -1], [8, 0],
    [5, 5], [5, -5], [6, 4], [6, -4],
        [7, 3], [7, -3], [8, 2], [8, -2], [9, 1], [9, -1], [10, 0],
    [12, 0])


def get_fringe_index(index):
    ''' Get (n, m) indices of the i-th Fringe Zernike polynomial '''
    if index < 1 or index > 37:
        raise ValueError('Index must be between 1 and 37 (inclusive)')
    return __fringe_zernike_index[index - 1]


def fringe_zernike(index, npix, outside=0.0):
    ''' Create a Zernike polynomial fringe pattern

    Arguments:
        index: int
            Fringe Zernike index (between 1 and 37, inclusive).

        npix: int
            Side length of the output array in pixels.

    Returns:
        zernike: ndarray
            Fringe Zernike wavefront of the specified index. The array is of
            shape (npix, npix). The outside of the aperture is set to zeros.
            Scaling is given in the Zero-to-Peak convention.
    '''
    return poppy_zernike(
        __fringe_zernike_index[index - 1][0],
        __fringe_zernike_index[index - 1][1],
        outside=outside,
        npix=npix,
        noll_normalize=False)


def noll_j_index(n, m):
    ''' Get the Noll index of the Zernike polynomial with (n, m) indices '''
    if n == 0:
        return 1

    c = [[1, 0, 1], [0, 1, 1]]
    p0 = (m >= 0) + (m == 0)
    p1 = ((n % 4) in (2, 3)) + 0
    return (n * (n + 1)) // 2 + abs(m) + c[p1][p0]


def noll_normalize(n, m, centering=True):
    ''' Normalize Zernike polynomial according to Noll convention '''
    if centering & (n <= 1):
        return np.inf
    elif m == 0:
        return np.sqrt(n + 1)
    else:
        return np.sqrt(2) * np.sqrt(n + 1)


def convert_fringe37_to_noll(coeff, centering=True):
    ''' Convert Fringe 37 coefficients to Noll coefficients

    Arguments:
        coeff: ndarray
            Coefficients of Zernike polynomials in Fringe 37 convention.

        centering: bool
            If True, the Zernike polynomials are centered at the origin.
            If False, the Zernike polynomials are centered at the center of
            the aperture.

    Returns:
        noll_coeff: ndarray
            Coefficients of Zernike polynomials in the Noll's convention.
    '''
    if len(coeff) > 37:
        raise ValueError('Coefficient array is too long')

    max_term = 79
    noll_coeff = np.zeros(max_term)

    for j, c in enumerate(coeff):
        n, m = get_fringe_index(j + 1)
        noll_j = noll_j_index(n, m)
        norm = noll_normalize(n, m, centering=centering)
        noll_coeff[noll_j - 1] = c / norm

    return noll_coeff
