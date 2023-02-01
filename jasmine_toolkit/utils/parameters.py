# -*- coding: utf-8 -*-
import math

import numpy as np
import pkg_resources

from jasmine_toolkit.datamodel.efficiency import Efficiency


# xxx_2

class Parameters:
    """This class is parameter holder

    The parameter holder class Parameters is implemented in Singleton pattern (see. GoF book).
    Below properties are defined.

    Properties:
    Only getter is implemented without attribute:
        aperture_inner_diameter, average_telescope_throughput, effective_focal_length, average_filter_efficiency,
        average_quantum_efficiency, total_efficiency, detector_format_x, detector_format_y, orbital_period, earth_mu,
        earth_c1, earth_c2, inclination, c_pix

    Only getter is implemented with attribute:
        orbital_eccentricity, num_detector_x, num_detector_y, pixel_sampling_frequency, (temporal)
        pixel_size, detector_separation_x, detector_separation_y, n_col_ch, n_row_ch, n_ch, n_ref_pix_right,
        n_ref_pix_left, n_ref_pix_top, n_ref_pix_bottom (Detector specification: confidential)
        maneuver_time, large_maneuver_time, (NEC report)

    Getter and Setter are implemented:
        effective_pupil_diameter, central_obscuration_ratio, short_wavelength_limit, orbital_altitude, window_size_x,
        window_size_y, (above values are temporal)
        saturation_magnitude, standard_magnitude, faint_end_magnitude, (temporal and should be defined by science
        requirements)
        f_number, (calculated from f = 4369mm when D = 360mm)
        full_well_electron, (defined at E2E meeting 8th Jun 2022 while referring JASMINE_HD_TN_HKZ_220501_01_detprop)
        attitude_control_error, exposure_time, (defined at E2E meeting 8th Jun 2022)
        long_wavelength_limit, read_out_noise, dark_current, (Kakenhi-report 26247029 and private communications)
        background_photon_flux, (JASMINE-C2-TN-RO-20220330-01-background)
        spider_type, spider_thickness, (temporal values, Reference TBD)
        optics_efficiency, quantum_efficiency, filter_efficiency (Read tables made by Kataza-san)

    internal attributes:
        EARTH_MASS, CONST_OF_GRAVITATION, EQUATORIAL_EARTH_RADIUS, POLAR_EARTH_RADIUS, EARTH_J2, ONE_YEAR,
        (above constants should be referred by other common libraries. Values are referred from internet.)
        cell_pix, use_M_flag, reference_wavelength
        (The value of cell_pix is defined in JASMINE-CA-TN-HKZ-001-01_DblMir2021c. The value of reference_wavelength
        is defined by E2E meeting May 25th 2022.)

    Not implemented yet
        saturation time, l_tan

    Known problem:
        Thread safety is not guaranteed.

    """

    __instance = None

    @staticmethod
    def get_instance():
        if Parameters.__instance is None:
            Parameters()
        return Parameters.__instance

    def __init__(self):
        if Parameters.__instance is None:
            Parameters.__instance = self
        else:
            raise Exception("Parameters is already instantiated.")
        self.__EARTH_MASS = 5.9724E24  # kg
        self.__CONST_OF_GRAVITATION = 6.6743E-11  # meter^3 kg^-1 s^-2
        self.__EQUATORIAL_EARTH_RADIUS = 6.3781E6  # meter
        self.__POLAR_EARTH_RADIUS = 6.3568E6  # meter
        self.__EARTH_J2 = 1.082632
        self.__ONE_YEAR = 31556926  # seconds
        self.__orbital_eccentricity = 0
        self.__effective_pupil_diameter = 0.36  # meter
        self.__central_obscuration_ratio = 0.35
        self.__f_number = 12.14
        self.__pixel_size = 1.0e-5  # meter
        self.__maneuver_time = 115  # second
        self.__large_maneuver_time = 220  # second
        self.__full_well_electron = 100000
# TODO: Definition of magnitude should be contains colour
        self.__saturation_magnitude = 10.0
        self.__standard_magnitude = 12.5
        self.__faint_end_magnitude = 14.5
# TODO: check whether attitude control error depends on exposure time or not.
        self.__attitude_control_error_mas = 300  # mas / 12.5 seconds
        self.__long_wavelength_limit = 1.6e-6  # meter
        self.__short_wavelength_limit = 1.0e-6  # meter
        self.__read_out_noise = 15  # electrons / read
        self.__dark_current = 25  # electrons / sec / pixel
        self.__background_photon_flux = 8  # electrons / sec / pixel
        self.__num_detector_x = 2
        self.__num_detector_y = 2
        self.__detector_separation_x = 0.02282  # meter old value is 0.02196
        self.__detector_separation_y = 0.02282  # meter the value is fixed by Y.Y. at Feb. 1st
        self.__orbital_altitude = 6.0E5  # meter
        self.__spider_type = ''
        self.__spider_thickness = 5e-3  # meter
        self.__window_size_x = 9
        self.__window_size_y = 9
        self.__pixel_sampling_frequency = 2e5  # Hz
        self.__n_col_ch = 123
        self.__n_row_ch = 1968
        self.__n_ch = 16
        self.__n_ref_pix_left = 8
        self.__n_ref_pix_right = 8
        self.__n_ref_pix_top = 8
        self.__n_ref_pix_bottom = 8
        self.__exposure_time = 12.5  # second(s)
# TODO: check it should be const or variable?
        self.__cell_pix = 13
        self.__use_M_flag = False
        self.__reference_wavelength = 1.4e-6
        spec_list = pkg_resources.resource_filename('jasmine_toolkit', 'data/teleff.json')
        self.__optics_efficiency = Efficiency.from_json(spec_list)
        # detector temperature
        spec_list = pkg_resources.resource_filename('jasmine_toolkit', 'data/qe/qe170.json')
        self.__quantum_efficiency = Efficiency.from_json(spec_list)
        # filter cut on wavelength ???
        f_name = "data/filter/filter" + str(int(self.__short_wavelength_limit * 1e8)).zfill(3) + ".json"
        spec_list = pkg_resources.resource_filename('jasmine_toolkit', f_name)
        self.__filter_efficiency = Efficiency.from_json(spec_list)

    @property
    def effective_pupil_diameter(self):
        return self.__effective_pupil_diameter

    def set_effective_pupil_diameter(self, value):
        self.__effective_pupil_diameter = value

    @property
    def central_obscuration_ratio(self):
        return self.__central_obscuration_ratio

    def set_central_obscuration_ratio(self, value):
        self.__central_obscuration_ratio = value

    @property
    def aperture_inner_diameter(self):
        return self.__effective_pupil_diameter * self.__central_obscuration_ratio

    @property
    def f_number(self):
        return self.__f_number

    def set_f_number(self, value):
        if self.__use_M_flag:
            raise Exception("M_flag is True and cannot set f_number.")
        self.__f_number = value

    def set_f_number_from_m(self, m):
        self.__use_M_flag = True
        self.__f_number = self.__pixel_size * m * 1000 / self.__cell_pix / self.__effective_pupil_diameter

    @property
    def effective_focal_length(self):
        return self.__f_number * self.__effective_pupil_diameter

    @property
    def pixel_size(self):
        return self.__pixel_size

    @property
    def maneuver_time(self):
        return self.__maneuver_time

    @property
    def large_maneuver_time(self):
        return self.__large_maneuver_time

    @property
    def full_well_electron(self):
        return self.__full_well_electron

    def set_full_well_electron(self, value):
        if value < 0:
            raise ValueError('full well electron should be positive.')
        self.__full_well_electron = value

    @property
    def saturation_magnitude(self):
        return self.__saturation_magnitude

    def set_saturation_magnitude(self, value):
        self.__saturation_magnitude = value

    @property
    def attitude_control_error_mas(self):
        return self.__attitude_control_error_mas

    def set_attitude_control_error_mas(self, value):
        if value < 0:
            raise ValueError('Attitude Control Error should be positive.')
        self.__attitude_control_error_mas = value

    @property
    def long_wavelength_limit(self):
        return self.__long_wavelength_limit

# TODO: long wavelength limit should be set from quantum_efficiency
    def set_long_wavelength_limit(self, value):
        assert self.__short_wavelength_limit < value
        self.__long_wavelength_limit = value

    @property
    def short_wavelength_limit(self):
        return self.__short_wavelength_limit

    def set_short_wavelength_limit(self, value):
        f_name = "data/filter/filter" + str(int(value * 1e8)).zfill(3) + ".json"
        spec_list = pkg_resources.resource_filename('telescope_baseline', f_name)
        self.__filter_efficiency = Efficiency.from_json(spec_list)
        self.__short_wavelength_limit = value

    @property
    def average_filter_efficiency(self):
        wave_ref = np.linspace(self.__short_wavelength_limit * 1e6, self.__long_wavelength_limit * 1e6, 1000)
        weight = np.ones(1000)
        return self.__filter_efficiency.weighted_mean(wave_ref, weight)

    @property
    def average_telescope_throughput(self):
        wave_ref = np.linspace(self.__short_wavelength_limit * 1e6, self.__long_wavelength_limit * 1e6, 1000)
        weight = np.ones(1000)
        return self.__optics_efficiency.weighted_mean(wave_ref, weight)

    @property
    def average_quantum_efficiency(self):
        wave_ref = np.linspace(self.__short_wavelength_limit * 1e6, self.__long_wavelength_limit * 1e6, 1000)
        weight = np.ones(1000)
        return self.__quantum_efficiency.weighted_mean(wave_ref, weight)

    @property
    def optics_efficiency(self):
        return self.__optics_efficiency

    def set_optics_efficiency(self, value):
        self.__optics_efficiency = value

    @property
    def filter_efficiency(self):
        return self.__filter_efficiency

    def set_filter_efficiency(self, value):
        self.__filter_efficiency = value

    @property
    def quantum_efficiency(self):
        return self.__quantum_efficiency

    def set_quantum_efficiency(self, value):
        self.__quantum_efficiency = value

    @property
    def total_efficiency(self):
        return self.average_telescope_throughput * self.average_filter_efficiency * self.average_quantum_efficiency

    @property
    def read_out_noise(self):
        return self.__read_out_noise

    def set_read_out_noise(self, value):
        self.__read_out_noise = value

    @property
    def dark_current(self):
        return self.__dark_current

    def set_dark_current(self, value):
        self.__dark_current = value

# TODO: The unit of background photon flux should be independent of diameter and band
    @property
    def background_photon_flux(self):
        return self.__background_photon_flux

    def set_background_photon_flux(self, value):
        self.__background_photon_flux = value

    @property
    def detector_format_x(self):
        return self.__n_row_ch - self.__n_ref_pix_top - self.__n_ref_pix_bottom

    @property
    def detector_format_y(self):
        return self.__n_col_ch * self.__n_ch - self.__n_ref_pix_left - self.__n_ref_pix_right

    @property
    def num_detector_x(self):
        return self.__num_detector_x

    @property
    def num_detector_y(self):
        return self.__num_detector_y

    @property
    def standard_magnitude(self):
        return self.__standard_magnitude

    def set_standard_magnitude(self, value):
        self.__standard_magnitude = value

    @property
    def faint_end_magnitude(self):
        return self.__faint_end_magnitude

    def set_faint_end_magnitude(self, value):
        self.__faint_end_magnitude = value

    @property
    def orbital_altitude(self):
        return self.__orbital_altitude

    def set_orbital_altitude(self, value):
        self.__orbital_altitude = value

    @property
    def orbital_period(self):
        return 2 * math.pi * math.pow(self.__EQUATORIAL_EARTH_RADIUS + self.orbital_altitude, 1.5) / math.sqrt(
            self.__CONST_OF_GRAVITATION * self.__EARTH_MASS)

    @property
    def earth_mu(self):
        return self.__CONST_OF_GRAVITATION * self.__EARTH_MASS

    @property
    def earth_c1(self):
        return -3 * math.pi * self.__EARTH_J2 * math.pow(self.__EQUATORIAL_EARTH_RADIUS / 1000, 2) \
               * self.__ONE_YEAR * math.sqrt(self.earth_mu) / 2 / math.pi * 180 / math.pi / math.pow(10000, 1.5)

    @property
    def earth_c2(self):
        return 360 / self.earth_c1

    @property
    def orbital_eccentricity(self):
        return self.__orbital_eccentricity

    @property
    def inclination(self):
        return math.acos(self.earth_c2 * math.pow((self.__EQUATORIAL_EARTH_RADIUS + self.__orbital_altitude) /
                                                  1000, 3.5)
                         * math.pow(1 - self.orbital_eccentricity * self.orbital_eccentricity, 2) * math.sqrt(1000))

    @property
    def spider_type(self):
        return self.__spider_type

    def set_spider_type(self, value):
        self.__spider_type = value

    @property
    def spider_thickness(self):
        return self.__spider_thickness

    def set_spider_thickness(self, value):
        self.__spider_thickness = value

    @property
    def window_size_x(self):
        return self.__window_size_x

    def set_window_size_x(self, value):
        self.__window_size_x = value

    @property
    def window_size_y(self):
        return self.__window_size_y

    def set_window_size_y(self, value):
        self.__window_size_y = value

    @property
    def n_col_ch(self):
        return self.__n_col_ch

    @property
    def n_row_ch(self):
        return self.__n_row_ch

    @property
    def n_ref_pix_left(self):
        return self.__n_ref_pix_left

    @property
    def n_ref_pix_right(self):
        return self.__n_ref_pix_right

    @property
    def n_ref_pix_top(self):
        return self.__n_ref_pix_top

    @property
    def n_ref_pix_bottom(self):
        return self.__n_ref_pix_bottom

    @property
    def n_ch(self):
        return self.__n_ch

    @property
    def pixel_sampling_frequency(self):
        return self.__pixel_sampling_frequency

    @property
    def detector_separation_x(self):
        return self.__detector_separation_x

    @property
    def detector_separation_y(self):
        return self.__detector_separation_y

    @property
    def exposure_time(self):
        return self.__exposure_time

    def set_exposure_time(self, value):
        self.__exposure_time = value

    @property
    def c_pix(self):
        return self.__reference_wavelength * self.__f_number / self.__pixel_size
