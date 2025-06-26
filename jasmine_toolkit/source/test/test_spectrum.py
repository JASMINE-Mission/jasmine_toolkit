#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for the spectrum module '''

from pytest import raises
from synphot.spectrum import SourceSpectrum

from ..spectrum import fetch_spectrum


def test_fetch_spectrum_valid_type():
    ''' Test that fetch_spectrum with a valid spectral type '''

    spectrum = fetch_spectrum('G2V', Av=0.0)
    assert isinstance(spectrum, SourceSpectrum)


def test_fetch_spectrum_invalid_type():
    ''' Test that fetch_spectrum with an invalid spectral type '''

    with raises(ValueError, match="Unknown spectral type"):
        fetch_spectrum('INVALID')
