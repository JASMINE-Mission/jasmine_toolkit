#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jasmine_toolkit.parameters as p


def test_dummy():
    print(p.naxis1)
    print(p.naxis2)
    print(p.detector.naxis1)
    p.naxis1 * 2
    assert False
