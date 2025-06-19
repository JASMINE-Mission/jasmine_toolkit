#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for filter module '''

from functools import cached_property
from synphot import SpectralElement

from jasmine_toolkit.optics.filter import FilterRegistry, registry


def test_all_filter_availability():
    filter_list = [
        name for name, attr in FilterRegistry.__dict__.items()
        if isinstance(attr, cached_property)]

    assert len(filter_list) > 0

    for name in filter_list:
        filter = getattr(registry, name)
        assert isinstance(filter, SpectralElement)
