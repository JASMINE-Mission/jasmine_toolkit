#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for filter module '''

from synphot import SpectralElement

from ..filter import REGISTRY


def test_filter_registry():
    ''' Test basic functions of the filter registry '''

    assert REGISTRY is not None
    assert isinstance(REGISTRY.jasmine_hw, SpectralElement)
