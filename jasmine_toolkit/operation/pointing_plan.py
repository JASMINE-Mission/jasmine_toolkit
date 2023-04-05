import math

import numpy as np
from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
from astropy.time import Time
from numpy import ndarray

from jasmine_toolkit.operation.fov_change_mode import EnumFovChangeMode
from jasmine_toolkit.utils.parameters import Parameters


class PointingPlan:
    def __init__(self):
        self.__grid = None
        self.__pointing: SkyCoord = None
        self.__grid_coord = None
        p: Parameters = Parameters.get_instance()
        detector_x = p.detector_format_x * (
                p.num_detector_x - 1) * p.pixel_size + p.detector_separation_x
        detector_y = p.detector_format_y * (
                p.num_detector_y - 1) * p.pixel_size + p.detector_separation_y
        self.__fov_x = detector_x / p.effective_focal_length
        self.__fov_y = detector_y / p.effective_focal_length
        detector_gap = p.detector_separation_x \
            - p.detector_format_x * p.pixel_size
        self.__gap_on_the_sky = detector_gap / p.effective_focal_length
        self._generate_grid()

    def add_entry(self, entry: np.ndarray) -> np.ndarray:
        pass

    def get_array(self) -> np.ndarray:
        # TODO This code is dangerous. copy function of numpy.ndarray
        #  automatically select deep or shallow copy, and is not controllable
        #  by user.  Return value should be a new object generated by deep
        #  copy. Some instruction show that use copy.deepcopy(ndarray) but
        #  error occurs.  Need to find appropriate method.
        return self.__grid

    def _generate_grid(self):
        """

        Returns: empty 3 dimensional list. The first and the second index
         denotes the location on the grid, and the components of the third
         index are [Time, number of observation].

        """
        p = Parameters.get_instance()
        l_min = p.minimum_l
        l_max = p.maximum_l
        b_min = p.minimum_b
        b_max = p.maximum_b
        n_l = int((l_max - l_min) / self.__gap_on_the_sky) + 1
        n_b = int((b_max - b_min) / self.__gap_on_the_sky) + 1
        self.__grid_coord = np.ndarray((n_l, n_b, 2))
        for i in range(n_l):
            for j in range(n_b):
                ll = l_min + self.__gap_on_the_sky * i
                b = b_min + self.__gap_on_the_sky * j
                c = SkyCoord(l=ll * u.rad, b=b * u.rad, frame='galactic')
                ra = c.icrs.ra.rad
                dec = c.icrs.dec.rad
                self.__grid_coord[i][j][0] = ra
                self.__grid_coord[i][j][1] = dec
        self.__grid = [[[] for i in range(n_b)] for j in range(n_l)]

    def find_next_pointing(self) -> SkyCoord:
        # TODO
        #   The code is implemented that always the algorithm is used for
        #   searching next FOV. It should be changed that successive two FOV
        #   should overlap half of its FOV.
        l0 = -1
        b0 = -1
        min_count = 100000
        n_l = len(self.__grid)
        n_b = len(self.__grid[0])
        for ll in range(n_l):
            for b in range(n_b):
                # tmp[ll][j] = len(self.__grid[ll][b])
                if len(self.__grid[ll][b]) < min_count:
                    min_count = len(self.__grid[ll][b])
                    l0 = ll
                    b0 = b
        p = Parameters.get_instance()
        coord_l = p.minimum_l + l0 * self.__gap_on_the_sky
        coord_b = p.minimum_b + b0 * self.__gap_on_the_sky
        self.__pointing = SkyCoord(l=coord_l * u.rad, b=coord_b * u.rad,
                                   frame='galactic')
        return self.__pointing

    def _coord_to_grid(self, coord: SkyCoord):
        coord_l = coord.galactic.l.rad
        coord_b = coord.galactic.b.rad
        if coord_l > math.pi:
            coord_l = coord_l - math.pi * 2
        p: Parameters = Parameters.get_instance()
        ll = (coord_l - p.minimum_l) / self.__gap_on_the_sky
        b = (coord_b - p.minimum_b) / self.__gap_on_the_sky
        if ll < 0 or ll >= len(self.__grid_coord)\
                or b < 0 or b >= len(self.__grid_coord[0]):
            return 0, 0
        return int(ll + 0.5), int(b + 0.5)

    def _grid_to_coord(self, ll: int, b: int):
        if ll < 0 or ll >= len(self.__grid_coord)\
                or b < 0 or b >= len(self.__grid_coord[0]):
            return SkyCoord(l=0 * u.rad, b=0 * u.rad, frame="galactic")
        return SkyCoord(ra=self.__grid_coord[ll][b][0] * u.rad,
                        dec=self.__grid_coord[ll][b][1] * u.rad, frame="icrs")

    def pointing_by_small_maneuver(self, pointing: SkyCoord,
                                   mode: EnumFovChangeMode):
        ll, b = self._coord_to_grid(pointing)
        if mode == EnumFovChangeMode.VERTICAL:
            b = b + int(self.__fov_y * 0.5 / self.__gap_on_the_sky)
        elif mode == EnumFovChangeMode.HORIZONTAL:
            ll = ll + int(self.__fov_x * 0.5 / self.__gap_on_the_sky)
        if b < 0:
            b = 0
        if b >= len(self.__grid[0]):
            b = len(self.__grid[0]) - 1
        if ll < 0:
            ll = 0
        if ll >= len(self.__grid):
            ll = len(self.__grid) - 1
        return SkyCoord(ra=self.__grid_coord[ll][b][0] * u.rad,
                        dec=self.__grid_coord[ll][b][1] * u.rad, frame='icrs')

    def make_observation(self, t: Time, pa: Angle, num_exposure: int):
        polygon = self._get_field_of_view(self.__pointing, pa)
        n_l = len(self.__grid)
        n_b = len(self.__grid[0])
        for ll in range(n_l):
            for b in range(n_b):
                if self.included_p(polygon, self.__grid_coord[ll][b]):
                    self.__grid[ll][b].append([t, num_exposure])

    @staticmethod
    def included_p(polygon: ndarray, target: ndarray):
        target = np.append(target, 0)
        z = np.zeros((len(polygon), 1))
        polygon = np.append(polygon, z, axis=1)
        win = 0
        for i in range(len(polygon)):
            j = i + 1
            if j > len(polygon) - 1:
                j = 0
            a0 = polygon[i] - target
            a1 = polygon[j] - target
            outer = np.cross(a0, a1) / (
                    np.linalg.norm(a0, ord=2) * np.linalg.norm(a1, ord=2))
            arg = outer[2]
            if arg > 1.0:
                arg = 1.0
            elif arg < -1.0:
                arg = -1.0
            win = win + math.asin(arg)
        if 0.1 > win > -0.1:
            return False
        else:
            return True

    def _get_field_of_view(self, pointing, pa):
        ne = np.array([self.__fov_x / 2, self.__fov_y / 2])
        se = np.array([self.__fov_x / 2, -self.__fov_y / 2])
        sw = np.array([-self.__fov_x / 2, -self.__fov_y / 2])
        nw = np.array([-self.__fov_x / 2, self.__fov_y / 2])
        rot = np.array(
            [[math.cos(pa), math.sin(pa)], [-math.sin(pa), math.cos(pa)]])
        po = np.array([pointing.icrs.ra.rad, pointing.icrs.dec.rad])
        ne = np.dot(rot, ne) + po
        se = np.dot(rot, se) + po
        sw = np.dot(rot, sw) + po
        nw = np.dot(rot, nw) + po
        return np.array([ne, se, sw, nw])
