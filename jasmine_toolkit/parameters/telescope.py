#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for the telescope/optics '''

import numpy as np

from .calclated_registry import calculated
from .utils import Parameter


__all__ = (
    'pupil_diameter',
    'f_number',
    'effective_focal_length',
    'central_obscuration',
    'field_of_view',
)


pupil_diameter = Parameter(
    'pupil_diameter',
    36,
    'cm',
    'the effective diameter of the primary mirror',
    'default value',
)

f_number = Parameter(
    'f_number',
    12.14,
    '',
    'the F-number of the optics',
    'default value',
)


@calculated
def effective_focal_length():
    import jasmine_toolkit.parameters as p
    effective_focal_length = p.telescope.f_number * p.telescope.pupil_diameter
    return Parameter(
        'effective_focal_length',
        value=effective_focal_length.to_value('mm'),
        unit='mm',
        description='Effective focal length of the optics',
        reference='calculated value')


central_obscuration = Parameter(
    'central_obscuration',
    0.35,
    '',
    'the obscuration by the secondary mirror in length ratio',
    'default value',
)


field_of_view = Parameter(
    'field_of_view',
    [0.55, 0.55],
    'degree',
    'the side lengths of the field of view',
    'default value',
)
