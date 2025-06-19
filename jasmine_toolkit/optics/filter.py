#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Define optical and infrared photometric bandpass filters '''

from dataclasses import dataclass
from functools import cached_property
from synphot import SpectralElement
from synphot.models import Empirical1D
from astroquery.svo_fps import SvoFps
import astropy.units as u

__all__ = [
    'compile_hw_band',
    'compile_2mass_band',
    'compile_euclid_band',
    'compile_gaia_band',
    'compile_roman_band',
    'compile_vista_band',
    'FilterRegistry',
    'REGISTRY',
]


__hw_band__ = {
    'wavelength': [
        0.20663, 0.21014, 0.21376, 0.21751, 0.22139, 0.22542, 0.22959,
        0.23392, 0.23842, 0.24310, 0.24796, 0.25302, 0.25829, 0.26379,
        0.26952, 0.27551, 0.28177, 0.28833, 0.29519, 0.30239, 0.30995,
        0.31790, 0.32626, 0.33508, 0.34439, 0.35423, 0.36465, 0.3757,
        0.37971, 0.38744, 0.39994, 0.41327, 0.42752, 0.44279, 0.45919,
        0.47398, 0.47685, 0.49592, 0.51658, 0.53904, 0.56355, 0.56826,
        0.59038, 0.61990, 0.65253, 0.66253, 0.68878, 0.72929, 0.75681,
        0.77487, 0.82653, 0.85108, 0.88557, 0.89822, 0.94535, 0.95369,
        1.03317, 1.03963, 1.12709, 1.13390, 1.22818, 1.23980, 1.32245,
        1.37756, 1.41673, 1.51100, 1.54871, 1.54975, 1.60527, 1.77114,
        1.88810, 2.06633
    ],
    'efficiency': [
        0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
        0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
        0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
        0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00,
        0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.9192e-07,
        3.6485e-06, 2.6752e-05, 1.2040e-04, 3.9891e-04, 1.0663e-03, 2.1371e-03,
        2.4130e-03, 4.4867e-03, 7.8575e-03, 1.3160e-02, 2.1183e-02, 2.3013e-02,
        3.1199e-02, 4.3691e-02, 6.0428e-02, 6.6424e-02, 8.3419e-02, 1.0969e-01,
        1.2595e-01, 1.4536e-01, 2.8057e-01, 3.9069e-01, 6.1326e-01, 7.2031e-01,
        8.2921e-01, 8.2670e-01, 8.0206e-01, 8.0000e-01, 8.0928e-01, 8.1000e-01,
        8.1000e-01, 8.0630e-01, 7.8000e-01, 7.6831e-01, 7.6000e-01, 7.3000e-01,
        7.1000e-01, 6.9694e-01, 0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00
    ]
}


def compile_band(facility, instrument, name):
    ''' Compile the bandpass data from SVO FPS'''
    table = SvoFps.get_transmission_data(f'{facility}/{instrument}.{name}')
    return SpectralElement(
        Empirical1D,
        points=table['Wavelength'], lookup_table=table['Transmission'])


def compile_hw_band():
    ''' Compile the JASMINE Hw bandpass filter '''
    return SpectralElement(
        Empirical1D,
        points=__hw_band__['wavelength'] * u.um,
        lookup_table=__hw_band__['efficiency'])


def compile_2mass_band(name):
    ''' Compile the 2MASS bandpass filter '''
    if name not in ('J', 'H', 'Ks'):
        raise ValueError(f'Unknown band name: {name}')
    return compile_band('2MASS', '2MASS', name)


def compile_euclid_band(name):
    ''' Compile the Euclid bandpass filter '''
    if name not in ('Y', 'J', 'H'):
        raise ValueError(f'Unknown band name: {name}')
    return compile_band('Euclid', 'NISP', name)


def compile_gaia_band(name):
    ''' Compile the Gaia (DR3) bandpass filter '''
    if name not in ('G', 'Gbp', 'Grp'):
        raise ValueError(f'Unknown band name: {name}')
    return compile_band('GAIA', 'GAIA3', name)


def compile_roman_band(name):
    ''' Compile the Roman bandpass filter '''
    if name not in ('F087', 'F106', 'F129', 'F158', 'F184', 'F213'):
        raise ValueError(f'Unknown band name: {name}')
    return compile_band('Roman', 'WFI', name)


def compile_vista_band(name):
    ''' Compile the VISTA bandpass filter '''
    if name not in ('Z', 'Y', 'J', 'H', 'Ks'):
        raise ValueError(f'Unknown band name: {name}')
    return compile_band('Paranal', 'VISTA', name)


@dataclass(frozen=True)
class FilterRegistry:

    @cached_property
    def jasmine_hw(self):
        return compile_hw_band()

    @cached_property
    def twomass_j(self):
        return compile_2mass_band('J')

    @cached_property
    def twomass_h(self):
        return compile_2mass_band('H')

    @cached_property
    def twomass_ks(self):
        return compile_2mass_band('Ks')

    @cached_property
    def euclid_y(self):
        return compile_euclid_band('Y')

    @cached_property
    def euclid_j(self):
        return compile_euclid_band('J')

    @cached_property
    def euclid_h(self):
        return compile_euclid_band('H')

    @cached_property
    def gaia_g(self):
        return compile_gaia_band('G')

    @cached_property
    def gaia_gbp(self):
        return compile_gaia_band('Gbp')

    @cached_property
    def gaia_grp(self):
        return compile_gaia_band('Grp')

    @cached_property
    def roman_f087(self):
        return compile_roman_band('F087')

    @cached_property
    def roman_f106(self):
        return compile_roman_band('F106')

    @cached_property
    def roman_f129(self):
        return compile_roman_band('F129')

    @cached_property
    def roman_f158(self):
        return compile_roman_band('F158')

    @cached_property
    def roman_f184(self):
        return compile_roman_band('F184')

    @cached_property
    def roman_f213(self):
        return compile_roman_band('F213')

    @cached_property
    def vista_z(self):
        return compile_vista_band('Z')

    @cached_property
    def vista_y(self):
        return compile_vista_band('Y')

    @cached_property
    def vista_j(self):
        return compile_vista_band('J')

    @cached_property
    def vista_h(self):
        return compile_vista_band('H')

    @cached_property
    def vista_ks(self):
        return compile_vista_band('Ks')


REGISTRY = FilterRegistry()
