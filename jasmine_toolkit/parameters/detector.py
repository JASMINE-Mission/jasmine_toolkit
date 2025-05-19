#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Parameters for detectors '''

import numpy as np
from .calclated_registry import calculated
from .utils import Parameter


__all__ = [
    'pixel_size',
    'pixel_scale',
    'full_well',
    'readout_noise',
    'dark_current',
    'n_column_channel',
    'n_row_channel',
    'n_channel',
    'naxis1_full',
    'naxis2_full',
    'naxis1',
    'naxis2',
    'n_reference_pixel_left',
    'n_reference_pixel_right',
    'n_reference_pixel_top',
    'n_reference_pixel_bottom',
    'alignment',
    'sampling_frequency',
    'minimum_readout_time',
]


pixel_size = Parameter(
    'pixel_size',
    10,
    'um',
    'the pixel scale of the detector.',
    'HPK CMOS design document (K51-B90034)',
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
        'degree/pixel',
        'the effective pixel scale on the sky',
        'calculated value',
    )


full_well = Parameter(
    'full_well',
    100000,
    'electron',
    'Full well size of the pixel in electron',
    'HPK CMOS design document (K51-B90034)',
)


readout_noise = Parameter(
    'readout_noise',
    41.0,
    'electron / pix',
    'Readout noise of the detector in electron',
    'tentative value',
)


dark_current = Parameter(
    'dark_current',
    25.0,
    'electron / (pix s)',
    'Dark current of the detector in electron/s',
    'tentative value',
)


n_column_channel = Parameter(
    'n_column_channel',
    123,
    'pixel',
    'number of columns per channel',
    'HPK CMOS design document (K51-B90034)',
)


n_row_channel = Parameter(
    'n_row_channel',
    1968,
    'pixel',
    'number of rows per channel',
    'HPK CMOS design document (K51-B90034)',
)


n_channel = Parameter(
    'n_channel',
    16,
    'pixel',
    'number of channels per detector',
    'HPK CMOS design document (K51-B90034)',
)


@calculated
def naxis1_full():
    import jasmine_toolkit.parameters.detector as d
    return Parameter(
        'naxis1_full',
        d.n_column_channel * d.n_channel,
        'pixel',
        'number of pixels along with NAXIS1',
        'calculated value',
    )


@calculated
def naxis2_full():
    import jasmine_toolkit.parameters.detector as d
    return Parameter(
        'naxis2_full',
        d.n_row_channel,
        'pixel',
        'number of pixels along with NAXIS2',
        'calculated value',
    )


@calculated
def naxis1():
    import jasmine_toolkit.parameters.detector as d
    n_ref = d.n_reference_pixel_left + d.n_reference_pixel_right
    return Parameter(
        'naxis1',
        d.naxis1_full - n_ref,
        'pixel',
        'number of pixels along with NAXIS1',
        'calculated value',
    )


@calculated
def naxis2():
    import jasmine_toolkit.parameters.detector as d
    n_ref = d.n_reference_pixel_top + d.n_reference_pixel_bottom
    return Parameter(
        'naxis2',
        d.naxis2_full - n_ref,
        'pixel',
        'number of pixels along with NAXIS2',
        'calculated value',
    )


n_reference_pixel_left = Parameter(
    'n_reference_pixel_left',
    8,
    'pixel',
    'number of reference pixels (left) per line',
    'HPK CMOS design document (K51-B90034)',
)


n_reference_pixel_right = Parameter(
    'n_reference_pixel_right',
    8,
    'pixel',
    'number of reference pixels (right) per line',
    'HPK CMOS design document (K51-B90034)',
)


n_reference_pixel_top = Parameter(
    'n_reference_pixel_top',
    8,
    'pixel',
    'number of reference pixels (top) per line',
    'HPK CMOS design document (K51-B90034)',
)


n_reference_pixel_bottom = Parameter(
    'n_reference_pixel_bottom',
    8,
    'pixel',
    'number of reference pixels (bottom) per line',
    'HPK CMOS design document (K51-B90034)',
)


alignment = Parameter(
    'alignment',
    [
        [[-1, +0, +21.33], [+0, -1, +21.33]],
        [[+0, +1, -21.33], [-1, +0, +21.33]],
        [[+1, +0, -21.33], [+0, +1, -21.33]],
        [[+0, -1, +21.33], [+1, +0, -21.33]],
    ],
    '',
    'coefficients of detector affine transformation',
    'MDR document (RPR-SJ430003B)',
)


sampling_frequency = Parameter(
    'sampling_frequency',
    2.0e5,
    'Hz',
    'pixel sampling frequency per channel',
    'HPK CMOS design document (K51-B90034)',
)


@calculated
def minimum_readout_time():
    import jasmine_toolkit.parameters.detector as d
    pixel_channel = d.n_column_channel * d.n_row_channel
    return Parameter(
        'minimum_readout_time',
        pixel_channel.value / d.sampling_frequency.to_value('Hz'),
        's',
        'minimum readout time',
        'calculated value',
    )
