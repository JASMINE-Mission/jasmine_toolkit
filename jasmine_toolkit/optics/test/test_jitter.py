#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for jitter module '''

from pytest import fixture
import numpy as np

from ..jitter import PSD_imagesim
from ..jitter import __get_resonance, ARMAModel, ARIMAModel, ACEModel


@fixture
def ar_coeff():
    f0 = 1.0 / 100.0
    return __get_resonance(
        [[0.999, f0 * 1], [0.999, f0 * 3], [0.999, f0 * 9]])


@fixture
def ma_coeff():
    f0 = 1.0 / 100.0
    return __get_resonance(
        [[0.990, f0 * 1], [0.993, f0 * 3], [0.995, f0 * 9]])


@fixture
def freq():
    return np.logspace(-3, 0, 100) / 2.0


def test_PSD_imagesim(freq):
    P = PSD_imagesim(freq)
    assert P.size == freq.size


def test_resonance():
    f0 = 1.0 / 100.0

    A = __get_resonance([[0.999, f0 * 1]])
    assert len(A) == 2

    A = __get_resonance([[0.999, f0 * 1], [0.999, f0 * 3]])
    assert len(A) == 4

    A = __get_resonance([[0.999, f0 * 1], [0.999, f0 * 3], [0.999, f0 * 9]])
    assert len(A) == 6


def test_arma_model(ar_coeff, ma_coeff, freq):
    arma = ARMAModel(ar_coeff, ma_coeff, 1.0)

    psd = arma.psd(freq)
    assert psd.shape == freq.shape

    sample = arma.generate(100)
    assert sample.shape == (100, )


def test_arima_model(ar_coeff, ma_coeff, freq):
    arima = ARIMAModel(ar_coeff, ma_coeff, 1.0, depth=1)

    psd = arima.psd(freq)
    assert psd.shape == freq.shape

    sample = arima.generate(100)
    assert sample.shape == (100, )


def test_ace_model(ar_coeff, ma_coeff, freq):
    ace = ACEModel(ar_coeff, ma_coeff, 1.0)

    sample = ace.generate(100)
    assert sample.shape == (100, )
