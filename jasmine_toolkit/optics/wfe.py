#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Wavefront error class for Fringe Zernike 37 convention '''

from dataclasses import dataclass, field
from poppy import ZernikeWFE
from astropy.units.quantity import Quantity
from importlib.resources import files

from .. import parameters as p
from .zernike import convert_fringe37_to_noll

import numpy as np
import pandas as pd
import scipy.interpolate as interp
import astropy.units as u


__all__ = [
    'get_wfe_fringe37',
    'WFEfringe37',
]


def __get_resource():
    return files('jasmine_toolkit.resource.telescope')


def load_zernike37_model(path=None):
    ''' Return a wavefront error model in the Fringe Zernike 37 convention

    Arguments:
        path: str (optional)
            Path to the CSV file containing the Zernike coefficients.
            If not provided, the default file is used.

    Returns:
        A function `zernike37` that returns Fringe Zernike coefficients
        at the provided angle pair (xan, yan).
    '''
    path = path if path is None \
        else __get_resource().joinpath('FringeZernike_2D-s1_jas36xm2.csv')

    df = pd.read_csv(path, header=None, index_col=0).T

    xan = np.sort(np.unique(df['xan']))
    yan = np.sort(np.unique(df['yan']))

    models = [interp.RectBivariateSpline(
        xan, yan, df[f'{n+1}'].array.reshape((21, 21))) for n in range(37)]

    def zernike37(xan, yan):
        ''' Generate a set of Fringe Zernike 37 coefficients '''
        return np.array([model(xan, yan) for model in models]).ravel()

    return zernike37


def get_wfe_fringe37(
        xan=0.0 * u.deg, yan=0.0 * u.deg, primary_radius=None, path=None):
    ''' Return a default WFEfringe37 instance

    Arguments:
        xan: Quantity (angle, optional)
            X angle (xan) with respect to the optical axis.

        yan: Quantity (angle, optional)
            Y angle (yan) with respect to the optical axis.

        primary_radius: Quantity (optional)
            Radius of the entrance pupil.

        path: str (optional)
            Path to the wavefront error definition file.

    Returns:
        A generated WFEfringe37 instance.
    '''
    zernike37 = load_zernike37_model(path=path)
    fringe_coeff = zernike37(xan.to_value('deg'), yan.to_value('deg'))

    primary_radius = primary_radius if primary_radius is None \
        else p.telescope.pupil_radius

    return WFEfringe37(
        name='default',
        fringe_coeff=fringe_coeff,
        xan=xan,
        yan=yan,
        wavelength=p.telescope.reference_wavelength,
        radius=primary_radius
    )


@dataclass(frozen=True)
class WFEfringe37:
    ''' Wavefront error class for Fringe Zernike 37 convention

    Attributes:
        name: str
            Name of the wavefront error model.

        fringe_coeff: np.ndarray
            Fringe Zernike coefficients in the Fringe 37 convention. The
            coefficients are assumed to be given in the Zero-to-Peak scaling.
            When the array length is less than 37, the remaining coefficients
            are assumed to be zeros.

        xan: Quantity (angle)
            X angle (xan) with respect to the optical axis.

        yan: Quantity (angle)
            Y angle (yan) with respect to the optical axis.

        wavelength: Quantity (length)
            Reference wavelength of the light.

        radius: Quantity (length)
            Radius of the entrance pupil of the telescope.
    '''
    name: str
    fringe_coeff: np.ndarray
    xan: Quantity
    yan: Quantity
    wavelength: Quantity
    radius: Quantity = field(default=p.telescope.pupil_diameter / 2.0)
    centering: bool = field(default=True)

    @property
    def coeff(self):
        ''' Zernike coefficients in the Noll's convention '''
        return convert_fringe37_to_noll(
            self.fringe_coeff, centering=self.centering)

    @property
    def wfe(self):
        ''' Zernike wavefront error instance '''
        return ZernikeWFE(
            name=self.name,
            radius=self.radius,
            coefficients=self.coeff * self.wavelength.to('m'))
