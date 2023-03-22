#!/usr/bin/env python
from .parameter import Parameter

__all__ = (
    'naxis1',
    'naxis2',
    'pixel_scale',
)

naxis1 = Parameter(
    'naxis1',
    1200,
    'pixel',
    'the NAXI1 size of the detector.',
    'default value',
)

naxis2 = Parameter(
    'naxis2',
    1200,
    'pixel',
    'the NAXIS2 size of the detector.',
    'default value',
)

pixel_scale = Parameter(
    'pixel_scale',
    10,
    'um',
    'the pixel scale of the detector.',
    'default value',
)
