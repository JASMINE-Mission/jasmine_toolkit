#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Miscellaneous functions '''

from astropy.coordinates import SkyCoord
from astropy.modeling.models import Polynomial2D, Legendre2D
from astropy.modeling.fitting import LinearLSQFitter
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np


__all__ = [
    'generate_grid',
    'get_residual',
    'visualize_difference',
]


def generate_grid(lon, lat, dlon=0.5, dlat=0.5, n_grids=31, frame='icrs'):
    ''' Generate grid points around the pointing direction

    Arguments:
        lon: `Quantity`
          The longitude of the poniting direction.

        lat: `Quantity`
          The latitude of the pointing direction.

        dlon: `float`
          The width of the grid area in degree.
          Defaults to 0.5.

        dlat: `float`
          The height of the grid area in degree.
          Defaults to 0.5.

        n_grids: `int`
          The number of grid points along with side.

    Returns:
        SkyCoord instance with sources alined in a grid.
    '''
    center = SkyCoord(lon, lat, frame=frame)
    lon_tics = np.linspace(-dlon / 2.0, dlon / 2.0, n_grids) * u.deg
    lat_tics = np.linspace(-dlat / 2.0, dlat / 2.0, n_grids) * u.deg
    lon, lat = np.meshgrid(lon_tics, lat_tics)
    lon = lon.flatten()
    lat = lat.flatten()
    return SkyCoord(
        center.spherical.lon + lon, center.spherical.lat + lat, frame=frame)


def get_residual(degree, xy, dxy, legendre=False):
    ''' Remove the distortion pattern using polynomial functions

    Arguments:
        degree: `float`
          The maximum order of the polynomial functions

        xy: `NDarray[n, 2]`
          Evaluation points on the focal plane coordinates.
          Used as explanatory variables in polynomial fitting.

        dxy: `NDarray[n, 2]`
          A distortion pattern on the focal plane coordinates.

        legendre: `boolean`
          Use the Legendre polynomial basis if true.

    Returns:
        The residual distortion pattern.
    '''
    xy = xy.copy() / 8000.0     # normalize the focal plane coordinate
    fitter = LinearLSQFitter()

    if legendre is True:
        model = Legendre2D(x_degree=degree, y_degree=degree)
    else:
        model = Polynomial2D(degree=degree)

    fit_x = fitter(model, x=xy[:, 0], y=xy[:, 1], z=dxy[:, 0])
    fit_y = fitter(model, x=xy[:, 0], y=xy[:, 1], z=dxy[:, 1])
    fitted = np.array(
        [fit_x(xy[:, 0], xy[:, 1]), fit_y(xy[:, 0], xy[:, 1])]).T

    return dxy - fitted


def visualize_difference(
        target, reference, output=None):
    ''' Visualize the differences of the footprints

    Arguments:
        target: `NDArray[n, 2]`

        reference: `NDArray[n, 2]`

        output: `str`
          The figure will be saved as the specified file.
    '''
    dv = target - reference

    pixel_size = 10 * u.um
    m1_diam = 36 * u.cm
    f_number = 12.14
    scale = np.atan2(pixel_size, m1_diam * f_number).to_value('degree')

    def rms(x):
        return np.sqrt(np.mean(x * x))

    def abm(x):
        return abs(x).max()

    def show_title(axis, v, unit=u.mas, comment=''):
        v = (v * scale * u.degree).to(unit)
        label_rms = f'rms: ({rms(v[:, 0]):.3f}, {rms(v[:, 1]):.3f})'
        label_max = f'max: ({abm(v[:, 0]):.3f}, {abm(v[:, 1]):.3f})'
        title = f'{label_rms}, {label_max}'.replace('u', r'$\mu$')
        axis.set_title(f'{comment}\n{title}', loc='left')

    fig, axes = plt.subplots(2, 2, figsize=(14, 14), sharex=True, sharey=True)

    ax = axes[0, 0]
    ax.quiver(reference[:, 0], reference[:, 1], dv[:, 0], dv[:, 1])
    ax.scatter(reference[:, 0], reference[:, 1], s=5, marker='.')
    show_title(ax, dv, 'arcsec', comment='no-correction')

    res = get_residual(0, reference, dv)
    ax = axes[0, 1]
    ax.quiver(reference[:, 0], reference[:, 1], res[:, 0], res[:, 1])
    ax.scatter(reference[:, 0], reference[:, 1], s=5, marker='.')
    show_title(ax, res, comment='0th-order correction')

    res = get_residual(1, reference, dv)
    ax = axes[1, 0]
    ax.quiver(reference[:, 0], reference[:, 1], res[:, 0], res[:, 1])
    ax.scatter(reference[:, 0], reference[:, 1], s=5, marker='.')
    show_title(ax, res, 'uas', comment='1st-order correction')

    res = get_residual(3, reference, dv)
    ax = axes[1, 1]
    ax.quiver(reference[:, 0], reference[:, 1], res[:, 0], res[:, 1])
    ax.scatter(reference[:, 0], reference[:, 1], s=5, marker='.')
    show_title(ax, res, 'uas', comment='3rd-order correction')

    fig.tight_layout()
    if output is not None: fig.savefig(output)
    plt.show()
