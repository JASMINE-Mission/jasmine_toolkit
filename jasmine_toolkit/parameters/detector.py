#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for detectors '''

import numpy as np
from .calclated_registry import calculated
from .utils  import Parameter


__all__ = (
    'naxis1',
    'naxis2',
    'pixel_size',
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

pixel_size = Parameter(
    'pixel_size',
    10,
    'um',
    'the pixel scale of the detector.',
    'default value',
)

@calculated
def pixel_scale():
    import jasmine_toolkit.parameters as p
    pix = p.detector.pixel_size
    efl = p.telescope.effective_focal_length
    pixel_scale = np.atan2(pix, efl)
    return Parameter(
        'pixel_scale',
        pixel_scale.to_value('degree'),
        'degree',
        'the effective pixel scale on the sky',
        'calculated value',
    )
