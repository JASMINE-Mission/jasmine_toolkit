#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for the satellite system '''

import numpy as np
from .calclated_registry import calculated
from .utils import Parameter


__all__ = [
  'attitude_control_error',
  'orbital_altitude',
  'earth_avoidance_angle_limit',
  'solar_face_angle_limit',
]


attitude_control_error = Parameter(
    'attitude_control_error',
    400,
    'mas',
    'typical satellite attitude control error in 12.5 sec',
    'Mission Design Report (RPR-SJ430003B)',
)


orbital_altitude = Parameter(
    'orbital_altitude',
    600,
    'km',
    'orbital altitude',
    'Mission Design Report (RPR-SJ430003B)',
)


earth_avoidance_angle_limit = Parameter(
    'earth_avoidance_angle_limit',
    25.7,
    'degree',
    'minimum earth avoidance angle',
    'Mission Design Report (RPR-SJ430003B)',
)


solar_face_angle_limit = Parameter(
    'solar_face_angle_limit',
    40.0,
    'degree',
    'maximum solar face angle',
    'Mission Design Report (RPR-SJ430003B)',
)
