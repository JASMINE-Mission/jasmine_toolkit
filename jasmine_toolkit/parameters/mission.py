#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for mission '''

import numpy as np
from .calclated_registry import calculated
from .utils import Parameter


__all__ = [
  'gcs_longitude_range',
  'gcs_latitude_range',
  'gcs_magnitude_range',
]


gcs_longitude_range = Parameter(
  'gcs_longitude_range',
  [-1.4, 0.7],
  'degree',
  'Galactic longitude range of the Galactic Center Astrometry Survey field',
  'MDR document (RPR-SJ430003B)',
)

gcs_latitude_range = Parameter(
  'gcs_latitude_range',
  [-0.6, 0.6],
  'degree',
  'Galactic latitude range of the Galactic Center Astrometry Survey field',
  'MDR document (RPR-SJ430003B)',
)

gcs_magnitude_range = Parameter(
  'gcs_magnitude_range',
  [9.5, 14.5],
  'mag',
  'Target magnitude range of the Galactic Center Astrometry Survey',
  'MDR document (RPR-SJ430003B)',
)
