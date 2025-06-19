#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for telescope module '''


import pytest
import astropy.units as u

from ..telescope import JASMINE


def test_jasmine_init_defaults():
    j = JASMINE()
    assert j.xan == pytest.approx(0.0 * u.deg)
    assert j.yan == pytest.approx(0.0 * u.deg)
    assert j.defocus == pytest.approx(0.0 * u.mm)
    assert j.name == 'JASMINE'
    assert j.wfe is not None


def test_jasmine_properties():
    j = JASMINE()
    # These properties are delegated to parameters,
    # just check they exist and are floats or quantities
    assert j.primary_aperture is not None
    assert j.obscuration is not None
    assert j.secondary_aperture is not None
    assert j.ref_wavelength is not None
    assert j.f_number is not None
    assert j.effective_focal_length is not None
    assert j.pixel_size is not None
    assert j.pixel_scale is not None
    assert j.wfe is not None


def test_jasmine_get_optical_system():
    j = JASMINE()
    optics = j.get_optical_system()
    assert hasattr(optics, 'add_pupil')
    assert hasattr(optics, 'add_detector')


def test_jasmine_get_filter_list():
    j = JASMINE()
    keys, mapper = j._get_filter_list()
    assert isinstance(keys, list)
    assert isinstance(mapper, dict)
    assert 'Hw' in keys
    assert 'jasmine_hw' in mapper.values()


def test_jasmine_synphot_bandpass_invalid():
    j = JASMINE()
    with pytest.raises(LookupError):
        j._get_synphot_bandpass('INVALID_FILTER')


def test_jasmine_filter_setter():
    j = JASMINE()
    valid_filter = j.filter_list[0]
    j.filter = valid_filter
    assert j.filter == valid_filter
    with pytest.raises(ValueError):
        j.filter = 'INVALID_FILTER'
