#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for filter module '''

from synphot import SpectralElement

from ..filter import REGISTRY, compile_hw_band


def test_compile_hw_band():
    band = compile_hw_band()
    assert isinstance(band, SpectralElement)

    # Check wavelength and efficiency arrays
    wave = band.waveset
    throughput = band(wave)
    assert len(wave) == len(throughput)
    assert (throughput >= 0).all() and (throughput <= 1).all()


def test_filter_registry():
    ''' Test basic functions of the filter registry '''

    assert REGISTRY is not None
    assert isinstance(REGISTRY.jasmine_hw, SpectralElement)
    assert isinstance(REGISTRY['jasmine_hw'], SpectralElement)
