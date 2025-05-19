#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Definition of the pupil plane '''

import jasmine_toolkit.parameters as p
import poppy
import numpy as np
import astropy.units as u


def get_obscuration(
        xan=0.0 * u.deg, yan=0.0 * u.deg,
        secondary_radius=None, n_supports=None, support_width=None,
        support_angle_offset=None):
    secondary_radius = secondary_radius \
        if secondary_radius else p.telescope.m2_obscuration_radius
    n_supports = n_supports \
        if n_supports else p.telescope.n_spider
    support_width = support_width \
        if support_width else p.telescope.spider_thickness
    support_angle_offset = support_angle_offset \
        if support_angle_offset else p.telescope.spider_angle_offset
    shift_x = 0 * u.mm
    shift_y = 0 * u.mm

    print(secondary_radius, p.telescope.m2_obscuration_radius)
    return poppy.SecondaryObscuration(
      secondary_radius=secondary_radius,
      n_supports=int(n_supports.value),
      support_width=support_width,
      support_angle_offset=support_angle_offset.to_value('deg'),
      shift_x=shift_x, shift_y=shift_y)
