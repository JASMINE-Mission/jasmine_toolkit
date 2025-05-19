#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' File description '''

from ..zernike import *

import pytest
import numpy as np


def test_get_fringe_index():
    ''' Test the get_fringe_index function '''
    for i in range(1, 38):
        n, m = get_fringe_index(i)
        assert n >= 0
        assert abs(m) <= n
        assert (n - abs(m)) % 2 == 0


def test_fringe_zernike():
    ''' Test the fringe_zernike function '''
    npix = 64
    for i in range(1, 38):
        zernike = fringe_zernike(i, npix)
        assert zernike.shape == (npix, npix)
        assert np.all(zernike <= 1)


def test_noll_j_index():
    ''' Test the noll_j_index function '''
    assert noll_j_index(0,  0) == 1
    assert noll_j_index(1,  1) == 2
    assert noll_j_index(1, -1) == 3
    assert noll_j_index(2,  0) == 4
    assert noll_j_index(2, -2) == 5
    assert noll_j_index(2,  2) == 6
    assert noll_j_index(3, -1) == 7
    assert noll_j_index(3,  1) == 8
    assert noll_j_index(3, -3) == 9
    assert noll_j_index(3,  3) == 10
    assert noll_j_index(4,  0) == 11
    assert noll_j_index(4,  2) == 12
    assert noll_j_index(4, -2) == 13
    assert noll_j_index(4,  4) == 14
    assert noll_j_index(4, -4) == 15
    assert noll_j_index(5,  1) == 16
    assert noll_j_index(5, -1) == 17
    assert noll_j_index(5,  3) == 18
    assert noll_j_index(5, -3) == 19
    assert noll_j_index(5,  5) == 20


def test_noll_normalize():
    ''' Test the noll_normalize function '''
    assert noll_normalize(0,  0) == np.inf
    assert noll_normalize(1,  1) == np.inf
    assert noll_normalize(1, -1) == np.inf
    assert noll_normalize(2,  0) == pytest.approx(np.sqrt(3))
    assert noll_normalize(2, -2) == pytest.approx(np.sqrt(6))
    assert noll_normalize(2,  2) == pytest.approx(np.sqrt(6))

    assert noll_normalize(0,  0, False) == pytest.approx(1)
    assert noll_normalize(1,  1, False) == pytest.approx(2)
    assert noll_normalize(1, -1, False) == pytest.approx(2)


def test_convert_fringe37_to_noll():
    ''' Test the convert_fringe37_to_noll function '''
    coeff = np.zeros(37)
    noll_coeff = convert_fringe37_to_noll(coeff)
    assert noll_coeff.shape == (79, )
