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
  'solar_separation_angle_limit',
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


solar_separation_angle_limit = Parameter(
    'solar_separation_angle_limit',
    40.0,
    'degree',
    'minimum solar separation angle',
    'Mission Design Report (RPR-SJ430003B)',
)


@calculated
def solar_separation_angle_range():
    import jasmine_toolkit.parameters.satellite as s
    import astropy.units as u
    angle = s.solar_separation_angle_limit.to_value('deg')
    return Parameter(
        'solar_separation_angle_range',
        value=[angle, 180.0 - angle],
        unit='deg',
        description='solar separation angle range',
        reference='calculated value',
    )
