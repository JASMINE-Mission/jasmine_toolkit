#!/usr/bin/env python
import numpy as np

from .parameter import Parameter


__all__ = (
    'effective_focal_length',
    'field_of_view',
    'tel_efficiency'
)

effective_focal_length = Parameter(
    'effective_focal_length',
    3776.0,
    'mm',
    'the effective focal length of the optics.',
    'default value',
)


# experimental parameter for array.
# it works. but array size cannot be changed
field_of_view = Parameter(
    'field_of_view',
    [30.0, 30.0],
    'arcmin',
    'the side lengths of the field of view',
    'default value',
)

# experimental parameter for structured quantity
# it works. but array size cannot be changed
_ = np.array([
    (0.1, 0.0),
    (0.2, 1.0),
    (0.3, 1.0),
    (0.4, 1.0),
    (0.5, 0.0),
], dtype=[('wavelength', 'f8'), ('efficiency', 'f8')])
tel_efficiency = Parameter(
    'tel_efficiency',
    _,
    'um, 1',
    '',
    'default value'
)
