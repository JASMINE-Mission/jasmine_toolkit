#!/usr/bin/env python
# -*- coding: utf-8 -*-
from poppy import Instrument
import poppy
import astropy.units as u
import numpy as np

from .filter import REGISTRY
from .pupil import get_pupil, get_wfe_fringe37
from .. import parameters as p


__all__ = [
  'JASMINE',
]


class JASMINE(Instrument):

    def __init__(
            self,
            xan=0.0 * u.deg,
            yan=0.0 * u.deg,
            defocus=0.0 * u.mm,
            wfe=None,
            fovsize=41,
            simsize=1024,
            fft_oversample=4,
            detector_oversample=4):
        super().__init__(name='JASMINE')

        self._xan = xan
        self._yan = yan
        self._defocus = defocus
        self._wfe = (
            wfe if wfe is not None else get_wfe_fringe37(xan, yan))

        self._fovsize = fovsize
        self._simsize = simsize
        self._fft_oversample = fft_oversample
        self._detector_oversample = detector_oversample

        self.optsys = self.get_optical_system()

    @property
    def primary_aperture(self):
        return p.telescope.pupil_radius

    @property
    def obscuration(self):
        return p.telescope.central_obscuration

    @property
    def secondary_aperture(self):
        return p.telescope.m2_obscuration_radius

    @property
    def ref_wavelength(self):
        return p.telescope.reference_wavelength

    @property
    def f_number(self):
        return p.telescope.f_number

    @property
    def effective_focal_length(self):
        return p.telescope.effective_focal_length

    @property
    def pixel_size(self):
        return p.detector.pixel_size

    @property
    def pixel_scale(self):
        return p.detector.pixel_scale

    @property
    def xan(self):
        return self._xan

    @property
    def yan(self):
        return self._yan

    @property
    def defocus(self):
        return self._defocus

    @property
    def wfe(self):
        return self._wfe

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, value):
        if value not in self.filter_list:
            raise ValueError(
                f'Instrument {self.name} doesn\'t have a filter "{value}".')
        self._filter = value

    def get_optical_system(
          self, fov_pixels=None, fov_arcsec=None,
          fft_oversample=None, detector_oversample=None, **args):

      optics = poppy.OpticalSystem(
          name='fake JASMINE',
          oversample=fft_oversample or self._fft_oversample,
          npix=self._simsize)

      optics.add_pupil(get_pupil(
          name='entrance pupil',
          xan=self._xan,
          yan=self._yan
      ))
      optics.add_detector(
          pixelscale=self.pixel_scale,
          fov_pixels=fov_pixels or self._fovsize,
          oversample=detector_oversample or self._detector_oversample)

      return optics

    def _calc_opd(self, z):
        return np.sqrt((self.focal_length + z)**2 + self.primary_aperture**2)

    def _get_default_nlambda(self, filtername):
        if filtername not in self.filter_list:
            raise LookupError(f'filter name {filtername} is not defined.')
        return 21

    def _get_default_fov(self):
        return (self.pixel_scale * self._fovsize * u.pixel).to_value('arcsec')

    def _get_filter_list(self):
        mapper = {
            'Hw': 'jasmine_hw',
            '2MASS_J': '2mass_j',
            '2MASS_H': '2mass_h',
            '2MASS_Ks': '2mass_ks',
            'Euclid_Y': 'euclid_y',
            'Euclid_J': 'euclid_j',
            'Euclid_H': 'euclid_h',
            'Gaia_G': 'gaia_g',
            'VISTA_Z': 'vista_z',
            'VISTA_Y': 'vista_y',
            'VISTA_J': 'vista_j',
            'VISTA_H': 'vista_h',
            'VISTA_Ks': 'vista_ks'
        }
        return list(mapper.keys()), mapper

    def _get_synphot_bandpass(self, filtername):
        if filtername not in self.filter_list:
            raise LookupError(f'filter name {filtername} is not defined.')
        return REGISTRY[filtername]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    j = JASMINE()

    fig, ax = plt.subplots(figsize=(10, 4))
    poppy.conf.default_image_display_fov = 10.0
    psf = j.calc_psf(display=True)
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 6))
    poppy.display_psf(
        psf, ax=ax, vmax=None, scale='asinh')
    plt.show()
