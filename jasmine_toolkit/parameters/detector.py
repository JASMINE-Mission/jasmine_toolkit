#!/usr/bin/env python
from .parameter import Parameter

__all__ = (
    'naxis1',
    'naxis2',
    'pixel_scale',
)

naxis1 = Parameter('naxis1', 1200, 'pixel', 'temp')
naxis2 = Parameter('naxis2', 1200, 'pixel', 'temp')
pixel_scale = Parameter('pixel_scale', 10, 'um', 'temp')
