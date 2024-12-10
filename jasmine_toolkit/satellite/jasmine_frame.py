#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' JASMINE reference frame '''

from astropy.coordinates.builtin_frames import BaseRADecFrame
from astropy.coordinates.attributes import TimeAttribute
from astropy.coordinates.attributes import QuantityAttribute
from astropy.coordinates.attributes import CartesianRepresentationAttribute
from astropy.coordinates.builtin_frames.utils import DEFAULT_OBSTIME
from astropy.coordinates.builtin_frames.icrs_cirs_transforms import \
    icrs_to_gcrs, gcrs_to_icrs

from astropy.coordinates import UnitSphericalRepresentation
from astropy.coordinates import CartesianRepresentation
from astropy.coordinates import BarycentricMeanEcliptic as Ecliptic
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.transformations import \
    FunctionTransformWithFiniteDifference

from astropy.coordinates import \
    get_body_barycentric_posvel as get_body_barycentric
from astropy.coordinates import ICRS, SkyCoord
from astropy.modeling.models import Polynomial2D, Legendre2D
from astropy.modeling.fitting import LinearLSQFitter

from astropy.wcs import WCS

import matplotlib.pyplot as plt
import astropy.constants as c
import astropy.units as u
import numpy as np

from .. import parameters as p


__all__ = [
    'JASMINEFrame',
    'HypotheticalFrame',
]

class _ObeservatoryMixin:
    def convert_topocentric(self, skycoord):
        ''' Convert to the topocentric direction

        Arguments:
            skycoord: SkyCoord
              SkyCoord object with the target sources, whose frame should be
              compatible with the instance.

        Results:
            A new SkyCoord object that contains the topocentric coordinates
            in the ICRS frame.
        '''
        return SkyCoord(skycoord.transform_to(self).spherical)

    def observe(self, skycoord):
        ''' An alias of convert_topocentric method '''
        return self.convert_topocentric(skycoord)


class _JASMINESpec:
    @property
    def plate_scale(self):
        ''' Provide the plate scale of JASMINE '''

        return p.pixel_scale / self.pixel_size

    @property
    def pixel_scale(self):
        ''' Provide the pixel scale of JASMINE '''

        return p.telescope.pixel_scale

    def wcs(self, lon, lat, pa=0.0*u.deg):
        ''' Generate the WCS instance for the JASMINE focal plane

        Arguments:
            lon: `Quantity`
            The longitude of the pointing direction.

            lat: `Quantity`
            The latitude of the pointing direction.
        Results:
            astropy.wcs.WCS object for the JASMINE telescope.
        '''
        scale = self.pixel_scale.to_value('degree')

        C = np.matrix([[np.cos(pa), -np.sin(pa)], [np.sin(pa), np.cos(pa)]])
        P = np.matrix([[-scale, 0.0], [0.0, scale]])

        wcsobj = WCS(naxis=2)
        wcsobj.wcs.ctype = ['RA---TAN', 'DEC--TAN']
        wcsobj.wcs.crval = [lon.value, lat.value]
        wcsobj.wcs.crpix = [1.0, 1.0]
        wcsobj.wcs.pc = C @ P

        return wcsobj


class HypotheticalFrame(BaseRADecFrame, _ObeservatoryMixin):
    ''' A coordinate or frame for a hypothetical observer in BCRS

    Parameters:
        obstime: `~astropy.time.Time`
          The time at which the observation is taken.  Used for determining the
          position of the Earth and its precession.

        obsbaryloc: `Quantity` or `CartesianRepresentation`
          The location of the observer relative to the Solar system barycenter.
          Defaults to [0, 0, 0], the Solar System barycenter.

        obsbaryvel: `Quantity` or `CartesianRepresentation`
          The observer velocity with respect to the Solar system barycenter.
          Defaults to [0, 0, 0], rest to the Solar System barycenter.
    '''

    obstime = TimeAttribute(
        default=DEFAULT_OBSTIME,
        doc='The reference time (time of observation)'
    )

    obsbaryloc = CartesianRepresentationAttribute(
        default=[0, 0, 0],
        unit=u.m,
        doc='Relative location with respect to the SSB'
    )

    obsbaryvel = CartesianRepresentationAttribute(
        default=[0, 0, 0],
        unit=u.m / u.s,
        doc='Relative velocity with respect to the SSB'
    )

    @property
    def obsgeoloc(self):
        earth_loc, _ = get_body_barycentric('Earth', self.obstime)
        return self.obsbaryloc - earth_loc

    @property
    def obsgeovel(self):
        _, earth_vel = get_body_barycentric('Earth', self.obstime)
        return self.obsbaryvel - earth_vel


frame_transform_graph.transform(
    FunctionTransformWithFiniteDifference,
    ICRS, HypotheticalFrame)(icrs_to_gcrs)


frame_transform_graph.transform(
    FunctionTransformWithFiniteDifference,
    HypotheticalFrame, ICRS)(gcrs_to_icrs)


class JASMINEFrame(BaseRADecFrame, _JASMINESpec, _ObeservatoryMixin):
    ''' A coordinate or frame for a hypothetical observer in BCRS

    Parameters:
        obstime: `~Time`
          The time at which the observation is taken. Used for determining
          the position of the Earth and its precession.

        phase: `~Quantity`
          The satellite orbital phase [0.0, 1.0].
          Defaults to 0.0,

        altitude: `~Quantity`
          The satellite altitude from the Earth's surface.
          Defaults to 600 km.

    '''

    obstime = TimeAttribute(
        default=DEFAULT_OBSTIME,
        doc='The reference time (time of observation)'
    )

    phase = QuantityAttribute(
        default=0.0,
        unit=u.one,
        doc='Orbital phase of the satellite'
    )

    altitude = QuantityAttribute(
        default=p.satellite.orbital_altitude,
        unit=u.km,
        doc='Orbital altitude of the satellite'
    )

    @property
    def orbital_radius(self):
        return c.R_earth + self.altitude

    @property
    def orbital_velocity(self):
        GM = c.G * c.M_earth
        return np.sqrt(GM / self.orbital_radius)

    @property
    def orbital_period(self):
        L = 2 * np.pi * self.orbital_radius
        return L / self.orbital_velocity

    @property
    def nadir_horizon_angle(self):
        return np.asin(c.R_earth / self.orbital_radius)

    @property
    def sun_direction(self):
        sun_loc, _ = get_body_barycentric('Sun', self.obstime)
        return self.__unit_cartesian(sun_loc - self.obsbaryloc)

    @property
    def ecliptic_longitude(self):
        observer = SkyCoord(self.obsbaryloc).transform_to(Ecliptic)
        return observer.lon

    def with_updated_phase(self):
        ''' Return a JASMINEFRame with updated phases '''
        t0 = np.atleast_1d(self.obstime)[0]
        p0 = np.atleast_1d(self.phase)[0]

        dt = np.atleast_1d(self.obstime) - t0
        phase = p0 + (dt / self.orbital_period).decompose()

        return self.__class__(
            obstime=self.obstime,
            phase=phase,
            altitude=self.altitude)

    def with_velocity_error(self, sigma, seed=42):
        ''' Return a new frame with disturbed velocity

        Arguments:
            sigma: Quantity
              The standard deviation of velocity noise. The value should be
              in units of velocity (e.g., m/s).

            seed: int
              The seed of the random number generator (default: 42).
        '''
        size = self.obsbaryvel.xyz.shape
        rng = np.random.default_rng(seed=seed)
        dv = CartesianRepresentation(rng.normal(0, 1, size=size) * sigma)
        t0 = self.obstime
        loc = self.obsbaryloc.copy()
        vel = self.obsbaryvel.copy() + dv

        return HypotheticalFrame(
            obstime=t0, obsbaryloc=loc, obsbaryvel=vel)

    def earth_separation(self, src):
        ''' Separation angle from the geocenter '''
        src = self.__unit_cartesian(src.icrs)
        geocen_dir = - self.__unit_cartesian(self.obsgeoloc)
        return np.arccos(src.xyz.T @ geocen_dir.xyz)

    def earth_avoidance(self, src):
        ''' Separation angle from the geocenter '''
        return self.earth_separation(src) - self.nadir_horizon_angle

    def sun_separation(self, src):
        ''' Separation angle from the sun '''
        src = self.__unit_cartesian(src.icrs)
        return np.arccos(src.xyz.T @ self.sun_direction.xyz)

    def observable(self, src,
                   sun_separation_angle=[45*u.deg, 135*u.deg],
                   earth_avoidance_angle=24.5*u.deg):
        ''' Check the target is observable '''
        ea = self.earth_avoidance(src)
        ss = self.sun_separation(src)
        return (ea > earth_avoidance_angle) \
            & (ss > sun_separation_angle[0]) & (ss < sun_separation_angle[1])

    @staticmethod
    def __unit_cartesian(obj):
        ''' Convert a Representation to a Unit Cartesian '''
        uobj = obj.represent_as(UnitSphericalRepresentation)
        return uobj.represent_as(CartesianRepresentation)

    @staticmethod
    def __quaternion(up, theta):
        ''' Generate a quaternion from a vector and rotation angle

        Arguments:
            up: `unit vector`
              The unit vector that defines the rotation axis.

            theta: `Quantity`, `Angle`
              The rotation angle.
        '''
        theta = np.ones(up.shape[1]) * theta
        return np.array([
            up[0] * np.sin(theta / 2), up[1] * np.sin(theta / 2),
            up[2] * np.sin(theta / 2),  np.cos(theta / 2)])

    @staticmethod
    def __qxp(q, p):
        ''' Calculate the product of two quaternions

        Arguments:
            q: `quaternion`
              The left-hand-side quaternion.

            p: `quaternion` or `vector`
              The right-hand-side quaternion or vector.
        '''
        if p.shape[0] == 3:
            p = np.pad(p, ((0, 1), (0, 0)))
        p = p.T.reshape((-1, 4, 1))
        qmat = np.moveaxis(np.array([
            [+q[3], -q[2], +q[1], +q[0]],
            [+q[2], +q[3], -q[0], +q[1]],
            [-q[1], +q[0], +q[3], +q[2]],
            [-q[0], -q[1], -q[2], +q[3]],
        ]), 2, 0)
        return (qmat @ p)[:, :, 0].T

    @staticmethod
    def __rotatev(v, u, theta):
        ''' Rotate the vector with respect to the unit vector

        Arguments:
            v: `vector`
              The vector element to be rotated.

            u: `unit vector`
              The unit vector, the axis of the rotations.

            theta: `Quantity`, `Angle`
              The rotation angle.
        '''
        if v.ndim == 1: v = np.expand_dims(v, 1)
        if u.ndim == 1: u = np.expand_dims(u, 1)

        theta = np.atleast_1d(theta)
        q = JASMINEFrame.__quaternion(u, +theta)
        p = JASMINEFrame.__quaternion(u, -theta)
        qxp = JASMINEFrame.__qxp

        return qxp(qxp(q, v), p)[:3, :]

    @property
    def obsgeoloc(self):
        earth_loc, earth_vel = get_body_barycentric('Earth', self.obstime)
        up = self.__unit_cartesian(earth_loc).xyz.value
        uv = self.__unit_cartesian(earth_vel).xyz.value

        p = JASMINEFrame.__rotatev(
            uv, up, -np.pi / 2.0 + 2 * np.pi * self.phase.value)

        return CartesianRepresentation(self.orbital_radius * p)

    @property
    def obsgeovel(self):
        earth_loc, earth_vel = get_body_barycentric('Earth', self.obstime)
        up = self.__unit_cartesian(earth_loc).xyz.value
        uv = self.__unit_cartesian(earth_vel).xyz.value

        v = JASMINEFrame.__rotatev(
            uv, up, 2 * np.pi * self.phase.value)

        return CartesianRepresentation(self.orbital_velocity * v)

    @property
    def obsbaryloc(self):
        earth_loc, _ = get_body_barycentric('Earth', self.obstime)
        return self.obsgeoloc + earth_loc

    @property
    def obsbaryvel(self):
        _, earth_vel = get_body_barycentric('Earth', self.obstime)
        return self.obsgeovel + earth_vel


frame_transform_graph.transform(
    FunctionTransformWithFiniteDifference,
    ICRS, JASMINEFrame)(icrs_to_gcrs)


frame_transform_graph.transform(
    FunctionTransformWithFiniteDifference,
    JASMINEFrame, ICRS)(gcrs_to_icrs)


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
