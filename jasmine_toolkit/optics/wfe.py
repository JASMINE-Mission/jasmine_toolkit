#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' File description '''

from dataclasses import dataclass, field
from poppy import ZernikeWFE
from astropy.units.quantity import Quantity

from .. import parameters as  p
from .zernike import convert_fringe37_to_noll

import numpy as np


@dataclass(frozen=True)
class WaveFrontError:
    ''' Wavefront error class for Fringe Zernike 37 convention

    Attributes:
        name: str
            Name of the wavefront error model.

        fringe_coeff: np.ndarray
            Fringe Zernike coefficients in the Fringe 37 convention. The
            coefficients are assumed to be given in the Zero-to-Peak scaling.
            When the array length is less than 37, the remaining coefficients
            are assumed to be zeros.

        xan: Quantity
            X angle (xan) with respect to the optical axis.

        yan: Quantity
            Y angle (yan) with respect to the optical axis.

        wavelength: Quantity
            Reference wavelength of the light.

        radius: Quantity
            Radius of the entrance pupil of the telescope.
    '''
    name: str
    fringe_coeff: np.ndarray
    xan: Quantity
    yan: Quantity
    wavelength: Quantity
    radius: Quantity = field(default=p.telescope.pupil_diameter / 2.0)

    @property
    def coeff(self):
        return convert_fringe37_to_noll(self.fringe_coeff)

    @property
    def wfe(self):
        return ZernikeWFE(
            name=self.name,
            radius=self.radius,
            coefficients=self.coeff * self.wavelength.to('m'))
