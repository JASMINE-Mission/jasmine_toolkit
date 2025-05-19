#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Definition of the pupil plane '''

import jasmine_toolkit.parameters as p
import poppy
import numpy as np
import astropy.units as u

from .wfe import get_wfe_fringe37


__all__ = [
    'get_obscuration',
    'get_pupil',
]


def __get_pupil(primary_radius=None):
    primary_radius = primary_radius \
        if primary_radius else p.telescope.pupil_radius
    return poppy.CircularAperture(
        radius=primary_radius, name='JASMINE entrance pupil')


def __get_obscuration(
        xan=0.0 * u.deg, yan=0.0 * u.deg, distance=0.0 * u.mm,
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

    shift_x = distance * np.tan(xan)
    shift_y = distance * np.tan(yan)

    return poppy.SecondaryObscuration(
      secondary_radius=secondary_radius,
      n_supports=int(n_supports.value),
      support_width=support_width,
      support_angle_offset=support_angle_offset.to_value('deg'),
      shift_x=shift_x, shift_y=shift_y)


def get_obscuration(
        xan=0.0 * u.deg, yan=0.0 * u.deg, distance=0.0 * u.mm,
        secondary_radius=None, n_supports=None, support_width=None,
        support_angle_offset=None):

    layer0 = __get_obscuration(
        xan=xan, yan=yan,
        distance=p.telescope.pupil_to_m2_distance,
        secondary_radius=secondary_radius, n_supports=n_supports,
        support_width=support_width, support_angle_offset=support_angle_offset)
    layer1 = __get_obscuration(
        xan=xan, yan=yan,
        distance=p.telescope.pupil_to_m2_distance + p.telescope.obscuration_depth,
        secondary_radius=secondary_radius, n_supports=n_supports,
        support_width=support_width, support_angle_offset=support_angle_offset)

    return poppy.CompoundAnalyticOptic([
        layer0,
        layer1
    ], name='JASMINE obscuration')


def get_pupil(
        primary_radius=None,
        xan=0.0 * u.deg, yan=0.0 * u.deg, distance=0.0 * u.mm,
        secondary_radius=None, n_supports=None, support_width=None,
        support_angle_offset=None):
    ''' Get the pupil plane '''

    pupil = __get_pupil(primary_radius=primary_radius)

    obscuration = get_obscuration(
        xan=xan, yan=yan, distance=distance,
        secondary_radius=secondary_radius, n_supports=n_supports,
        support_width=support_width, support_angle_offset=support_angle_offset)

    wfe_fringe = get_wfe_fringe37(
        xan=xan, yan=yan, primary_radius=primary_radius)

    return poppy.CompoundAnalyticOptic([
        wfe_fringe.wfe,
        pupil,
        obscuration
    ], name='entrance pupil')
