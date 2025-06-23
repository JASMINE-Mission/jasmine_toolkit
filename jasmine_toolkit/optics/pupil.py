#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Definition of the pupil plane '''

import jasmine_toolkit.parameters.telescope as tel
import poppy
import numpy as np
import astropy.units as u

from .wfe import get_wfe_fringe37, WFEfringe37


__all__ = [
    'get_obscuration',
    'get_pupil',
]


def __calc_optical_path(offset=0.0 * u.mm):
    return np.hypot(tel.effective_focal_length + offset, tel.pupil_radius)


def __calc_defocus_nwave(offset, wavelength):
    delta = offset - __calc_optical_path(offset) + __calc_optical_path()
    return delta.to_value('mm') / wavelength.to_value('mm')


def __get_pupil(primary_radius):
    ''' Helper function to generate a circular aperture '''

    return poppy.CircularAperture(
        radius=primary_radius, name='JASMINE entrance pupil')


def __get_defocus_element(offset, wavelength, radius):
    ''' Helper function to generate a defocus element '''

    return poppy.ThinLens(
        nwaves=__calc_defocus_nwave(offset, wavelength),
        reference_wavelength=wavelength,
        radius=radius,
        name='defocus element')


def __get_obscuration(
        xan, yan, distance,
        secondary_radius, n_supports, support_width,
        support_angle_offset):
    ''' Helper function to generate the secondary obscuration '''

    shift_x = distance * np.tan(xan)
    shift_y = distance * np.tan(yan)

    return poppy.SecondaryObscuration(
      secondary_radius=secondary_radius,
      n_supports=n_supports,
      support_width=support_width,
      support_angle_offset=support_angle_offset.to_value('deg'),
      shift_x=shift_x, shift_y=shift_y)


def get_obscuration(
        xan, yan,
        secondary_radius,
        pupil_to_m2_distance,
        obscuration_depth,
        n_supports,
        support_width,
        support_angle_offset):
    ''' Obtain the obscuration mask at the entrance pupil

    Arguments:
        xan: Quantity (angle)
            X angle (xan) with respect to the optical axis.

        yan: Quantity (angle)
            Y angle (yan) with respect to the optical axis.

        secondary_radius: Quantity (length)
            Radius of the secondary mirror.

        pupil_to_m2_distance: Quantity (length)
            Distance from the entrance pupil to the secondary mirror.

        obscuration_depth: Quantity (length)
            Depth of the obscuration.

        n_supports: int
            Number of support struts.

        support_width: Quantity (length)
            Width of the support struts.

        support_angle_offset: Quantity (angle)
            Angle offset of the support struts.

    Returns:
        A two-layer obscuration mask pattern.
    '''

    options = {
        'xan': xan,
        'yan': yan,
        'secondary_radius': secondary_radius,
        'n_supports': n_supports,
        'support_width': support_width,
        'support_angle_offset': support_angle_offset
    }

    layer0 = __get_obscuration(
        distance=pupil_to_m2_distance, **options)
    layer1 = __get_obscuration(
        distance=pupil_to_m2_distance + obscuration_depth, **options)

    return poppy.CompoundAnalyticOptic(
        [layer0, layer1], name='JASMINE obscuration')


def get_pupil(
        name='entrance pupil',
        xan=0.0 * u.deg,
        yan=0.0 * u.deg,
        defocus=0.0 * u.mm,
        primary_radius=None,
        pupil_to_m2_distance=None,
        obscuration_depth=None,
        secondary_radius=None,
        n_supports=None,
        support_width=None,
        support_angle_offset=None,
        reference_wavelength=None,
        wfe=None):
    ''' Generate a set of optical elements at the pupil plane

    Options:
        name: str
            Name of the entrance pupil.

        xan: Quantity (angle)
            X angle (xan) with respect to the optical axis.

        yan: Quantity (angle)
            Y angle (yan) with respect to the optical axis.

        primary_radius: Quantity (length)
            Radius of the entrance aperture.

        pupil_to_m2_distance: Quantity (length)
            Distance from the entrance pupil to the secondary mirror.

        obscuration_depth: Quantity (length)
            Depth of the obscuration.

        secondary_radius: Quantity (length)
            Radius of the secondary mirror.

        n_supports: int
            Number of support struts.

        support_width: Quantity (length)
            Width of the support struts.

        support_angle_offset: Quantity (angle)
            Angle offset of the support struts.

        wfe: ZernikeWFE or WFEfringe37
            Definition of the wavefront error at the entrance pupil.

    Returns:
        A compound analytic optic instance for the JASMINE telescope.
    '''

    primary_radius = (
        primary_radius if primary_radius is not None
        else tel.pupil_radius)
    secondary_radius = (
        secondary_radius if secondary_radius is not None
        else tel.m2_obscuration_radius)
    n_supports = (
        n_supports if n_supports is not None
        else tel.n_spider)
    support_width = (
        support_width if support_width is not None
        else tel.spider_thickness)
    support_angle_offset = (
        support_angle_offset if support_angle_offset is not None
        else tel.spider_angle_offset)
    pupil_to_m2_distance = (
        pupil_to_m2_distance if pupil_to_m2_distance is not None
        else tel.pupil_to_m2_distance)
    obscuration_depth = (
        obscuration_depth if obscuration_depth is not None
        else tel.obscuration_depth)
    reference_wavelength = (
        reference_wavelength if reference_wavelength is not None
        else tel.reference_wavelength)

    pupil = __get_pupil(primary_radius=primary_radius)

    obscuration = get_obscuration(
        xan=xan, yan=yan,
        pupil_to_m2_distance=pupil_to_m2_distance,
        obscuration_depth=obscuration_depth,
        secondary_radius=secondary_radius,
        n_supports=int(n_supports),
        support_width=support_width,
        support_angle_offset=support_angle_offset)

    defocus = __get_defocus_element(
        offset=defocus,
        wavelength=reference_wavelength,
        radius=primary_radius)

    if wfe is None:
        wfe_fringe = get_wfe_fringe37(
            xan=xan, yan=yan, primary_radius=primary_radius)
        wfe = wfe_fringe.wfe
    elif isinstance(wfe, poppy.ZernikeWFE):
        wfe = wfe
    elif isinstance(wfe, WFEfringe37):
        wfe = wfe.wfe

    return poppy.CompoundAnalyticOptic(
        [wfe, pupil, obscuration, defocus], name=name)
