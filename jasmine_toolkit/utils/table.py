#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Functions to dump a parameter table '''

import os
import numpy as np
import jasmine_toolkit.parameters as p


__items__ = [
    # telescope
    p.telescope.pupil_diameter,
    p.telescope.central_obscuration,
    p.telescope.f_number,
    p.telescope.effective_focal_length,
    p.telescope.n_spider,
    p.telescope.spider_thickness,
    p.telescope.field_of_view,

    # detector
    p.detector.naxis1,
    p.detector.naxis2,
    p.detector.naxis1_full,
    p.detector.naxis2_full,
    p.detector.n_channel,
    p.detector.n_column_channel,
    p.detector.n_row_channel,
    p.detector.n_reference_pixel_left,
    p.detector.n_reference_pixel_right,
    p.detector.n_reference_pixel_top,
    p.detector.n_reference_pixel_bottom,
    p.detector.readout_noise,
    p.detector.dark_current,
    p.detector.sampling_frequency,
    p.detector.minimum_readout_time,

    # satellite
    p.satellite.attitude_control_error,
    p.satellite.earth_avoidance_angle_limit,
    p.satellite.solar_face_angle_limit,

    # misison
    p.mission.gcs_longitude_range,
    p.mission.gcs_latitude_range,
    p.mission.gcs_magnitude_range,
]

__description__ = ''' Dump a parameter table for the DokuWiki
'''


def __table_header():
    return 'Parameter List\n\n^Name ^Value ^Units ^Comments^\n'


def __table_item_template(name, value, unit, reference):
    if isinstance(value, np.ndarray):
        value = str(value)
        return f'| {name:28s} | {value:>16} | {unit:18} | {reference:24s} |\n'
    elif isinstance(value, float):
        return f'| {name:28s} | {value:16.2f} | {unit:18} | {reference:24s} |\n'
    else:
        return f'| {name:28s} | {value:16} | {unit:18} | {reference:24s} |\n'


def dump_table(output=None, overwrite=False, **options):
    table = __table_header()

    for p in __items__:
        table += __table_item_template(
            p.name, p.value, p.unit, p.reference)

    if output is None:
        print(table.strip())
    else:
        if os.path.exists(output) and overwrite is False:
            raise FileExistsError(f'File "{output}" already exists')
        with open(output, 'tw') as fp:
            fp.write(table)


def setup_parser(parser):
    parser.add_argument(
       'output', nargs='?',
       help='output file')
    parser.add_argument(
       '-f', '--overwrite',
       action='store_true',
       help='overwrite if the output file exists')


if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser as ap
    parser = ap(description=__description__)

    setup_parser(parser)
    args = parser.parse_args(sys.argv[1:])
    dump_table()
