#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for the telescope/optics '''

from .calclated_registry import calculated
from .utils import Parameter


__all__ = (
    'pupil_diameter',
    'pupil_radius',
    'f_number',
    'effective_focal_length',
    'central_obscuration',
    'm2_obscuration_radius',
    'pupil_to_m2_distance',
    'obscuration_depth',
    'field_of_view',
    'n_spider',
    'spider_thickness',
    'spider_angle_offset',
    'reference_wavelength',
)


pupil_diameter = Parameter(
    'pupil_diameter',
    36,
    'cm',
    'the effective diameter of the primary mirror',
    'jas36xm2_as35',
)


@calculated
def pupil_radius():
    import jasmine_toolkit.parameters as p
    radius = p.telescope.pupil_diameter / 2.0
    return Parameter(
        'pupil_radius',
        value=radius.to_value('mm'),
        unit='mm',
        description='Effective radius of the pupil',
        reference='calculated value')


f_number = Parameter(
    'f_number',
    12.14,
    '',
    'the F-number of the optics',
    'jas36xm2_as35',
)


@calculated
def effective_focal_length():
    import jasmine_toolkit.parameters.telescope as t
    effective_focal_length = t.f_number * t.pupil_diameter
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
    'jas36xm2_as35',
)


pupil_to_m2_distance = Parameter(
    'pupil_to_m2_distance',
    227.0,
    'mm',
    'the distance from the pupil to the secondary mirror',
    'jas36xm2_as35',
)


obscuration_depth = Parameter(
    'obscuration_depth',
    50.0,
    'mm',
    'the depth of the obscuration layer',
    'jas36xm2_as35',
)


@calculated
def m2_obscuration_radius():
    import jasmine_toolkit.parameters.telescope as t
    radius = t.central_obscuration * t.pupil_radius
    return Parameter(
        'm2_obscuration_radius',
        value=radius.to_value('mm'),
        unit='mm',
        description='Radius of the secondary mirror obscuration',
        reference='calculated value')


field_of_view = Parameter(
    'field_of_view',
    [0.55, 0.55],
    'degree',
    'the side lengths of the field of view',
    'Mission Design Report (RPR-SJ430003B)',
)


n_spider = Parameter(
    'n_spider',
    3,
    '',
    'number of the secondary mirror supports',
    'jas36xm2_as35',
)


spider_thickness = Parameter(
    'spider_thickness',
    10.0,
    'mm',
    'thickness of the secondary mirror supports',
    'jas36xm2_as35',
)


spider_angle_offset = Parameter(
    'spider_angle_offset',
    0.0,
    'degree',
    'rotation angle of the secondary mirror supports',
    'tentative value',
)


reference_wavelength = Parameter(
    'reference_wavelength',
    1.25,
    'um',
    'reference wavelength for the optics design',
    'jas36xm2_as35',
)
