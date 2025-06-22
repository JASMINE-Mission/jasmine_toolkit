#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for filter module '''

from functools import cached_property
from synphot import SpectralElement

from jasmine_toolkit.optics.filter import FilterRegistry, REGISTRY


def test_all_filter_attributes():
    ''' Test that all filter attributes in the registry '''

    filter_list = [
        name for name, attr in FilterRegistry.__dict__.items()
        if isinstance(attr, cached_property)]

    assert len(filter_list) > 0

    for name in filter_list:
        band = getattr(REGISTRY, name)
        assert isinstance(band, SpectralElement)


def test_all_filter_getitem():
    ''' Test the __getitem__ method of the filter registry '''

    for name in REGISTRY.keys():
        band = REGISTRY[name]
        assert isinstance(band, SpectralElement)
