from astropy.constants import Constant
import math
import pkg_resources
import numpy as np
import warnings
from jasmine_toolkit.datamodel.efficiency import Efficiency
from jasmine_toolkit.utils.parameters2 import Parameters2, constant_formula


class JasmineConstant(Constant):
    # TODO 規格の切り返したい場合は、このクラスから切り離した方が良いです
    # 規格の切り替えはこの辺で行ってます
    # see https://onl.sc/BTGXenG (astropyのconfig.py)
    default_reference = "JASMINE"
    _registry = {}
    _has_incompatible_units = set()


def __p():
    return Parameters2()


EARTH_MASS = JasmineConstant(
    "EARTH_MASS", "Earth mass", 5.9724E24, "kg", 0.0
)

CONST_OF_GRAVITATION = JasmineConstant(
    "CONST_OF_GRAVITATION", "CONST_OF_GRAVITATION",
    6.6743E-11, "m3 / (kg s2)", 0.0
)

EQUATORIAL_EARTH_RADIUS = JasmineConstant(
    "EQUATORIAL_EARTH_RADIUS", "EQUATORIAL_EARTH_RADIUS", 6.3781E6, "m", 0.0
)

POLAR_EARTH_RADIUS = JasmineConstant(
    "POLAR_EARTH_RADIUS", "POLAR_EARTH_RADIUS", 6.3568E6, "m", 0.0
)

EARTH_J2 = JasmineConstant(
    "EARTH_J2", "EARTH_J2", 1.082632, "", 0.0
)

ONE_YEAR = JasmineConstant(
    "ONE_YEAR", "ONE_YEAR", 31556926, "s", 0.0
)

orbital_eccentricity = JasmineConstant(
    "orbital_eccentricity", "orbital_eccentricity", 0, "", 0.0
)

effective_pupil_diameter = JasmineConstant(
    "effective_pupil_diameter", "effective_pupil_diameter", 0.36, "m", 0.0
)

central_obscuration_ratio = JasmineConstant(
    "central_obscuration_ratio", "central_obscuration_ratio", 0.35, "", 0.0
)

f_number = JasmineConstant(
    "f_number", "f_number", 12.14, "", 0.0
)

pixel_size = JasmineConstant(
    "pixel_size", "pixel_size", 1.0e-5, "m", 0.0
)

maneuver_time = JasmineConstant(
    "maneuver_time", "maneuver_time", 115, "s", 0.0
)

large_maneuver_time = JasmineConstant(
    "large_maneuver_time", "large_maneuver_time", 220, "s", 0.0
)

full_well_electron = JasmineConstant(
    "full_well_electron", "full_well_electron", 100000, "s", 0.0
)

# TODO: Definition of magnitude should be contains colour

saturation_magnitude = JasmineConstant(
    "saturation_magnitude", "saturation_magnitude", 10.0, "", 0.0
)

standard_magnitude = JasmineConstant(
    "standard_magnitude", "standard_magnitude", 12.5, "", 0.0
)

faint_end_magnitude = JasmineConstant(
    "faint_end_magnitude", "faint_end_magnitude", 14.5, "", 0.0
)

# TODO: check whether attitude control error depends on exposure time or not.

attitude_control_error_mas = JasmineConstant(
    "attitude_control_error_mas", "attitude_control_error_mas", 300, "", 0.0
)   # mas / 12.5 seconds

long_wavelength_limit = JasmineConstant(
    "long_wavelength_limit", "long_wavelength_limit", 1.6e-6, "m", 0.0
)

short_wavelength_limit = JasmineConstant(
    "short_wavelength_limit", "short_wavelength_limit", 1.0e-6, "m", 0.0
)

read_out_noise = JasmineConstant(
    "read_out_noise", "read_out_noise", 15, "", 0.0
)   # electrons / read

dark_current = JasmineConstant(
    "dark_current", "dark_current", 25, "", 0.0
)   # electrons / sec / pixel

background_photon_flux = JasmineConstant(
    "background_photon_flux", "background_photon_flux", 8, "", 0.0
)   # electrons / sec / pixel

num_detector_x = JasmineConstant(
    "num_detector_x", "num_detector_x", 2, "", 0.0
)

num_detector_y = JasmineConstant(
    "num_detector_y", "num_detector_y", 2, "", 0.0
)

detector_separation_x = JasmineConstant(
    "detector_separation_x", "detector_separation_x", 0.02282, "m", 0.0
)   # old value is 0.02196

detector_separation_y = JasmineConstant(
    "detector_separation_y", "detector_separation_y", 0.02282, "m", 0.0
)   # the value is fixed by Y.Y. at Feb. 1st

orbital_altitude = JasmineConstant(
    "orbital_altitude", "orbital_altitude", 6.0E5, "m", 0.0
)

spider_type = ''

spider_thickness = JasmineConstant(
    "spider_thickness", "spider_thickness", 5e-3, "m", 0.0
)

window_size_x = JasmineConstant(
    "window_size_x", "window_size_x", 9, "", 0.0
)

window_size_y = JasmineConstant(
    "window_size_y", "window_size_y", 9, "", 0.0
)

pixel_sampling_frequency = JasmineConstant(
    "pixel_sampling_frequency", "pixel_sampling_frequency", 2e5, "Hz", 0.0
)

n_col_ch = JasmineConstant(
    "n_col_ch", "n_col_ch", 123, "", 0.0
)

n_row_ch = JasmineConstant(
    "n_row_ch", "n_row_ch", 1968, "", 0.0
)

n_ch = JasmineConstant(
    "n_ch", "n_ch", 16, "", 0.0
)

n_ref_pix_left = JasmineConstant(
    "n_ref_pix_left", "n_ref_pix_left", 8, "", 0.0
)

n_ref_pix_right = JasmineConstant(
    "n_ref_pix_right", "n_ref_pix_right", 8, "", 0.0
)

n_ref_pix_top = JasmineConstant(
    "n_ref_pix_top", "n_ref_pix_top", 8, "", 0.0
)

n_ref_pix_bottom = JasmineConstant(
    "n_ref_pix_bottom", "n_ref_pix_bottom", 8, "", 0.0
)

exposure_time = JasmineConstant(
    "exposure_time", "exposure_time", 12.5, "s", 0.0
)

ltan = JasmineConstant(
    "ltan", "ltan", 6, "h", 0.0
)

# TODO: check it should be const or variable?

cell_pix = JasmineConstant(
    "cell_pix", "cell_pix", 13, "", 0.0
)

use_M_flag = False

reference_wavelength = JasmineConstant(
    "reference_wavelength", "reference_wavelength", 1.4e-6, "", 0.0
)


def __make_optics_efficiency():
    spec_list = pkg_resources.resource_filename(
        'jasmine_toolkit', 'data/teleff.json')
    return Efficiency.from_json(spec_list)


optics_efficiency = __make_optics_efficiency()


def __make_quantum_efficiency():
    spec_list = pkg_resources.resource_filename(
        'jasmine_toolkit', "data/qe/qe170.json")
    return Efficiency.from_json(spec_list)


quantum_efficiency = __make_quantum_efficiency()


@constant_formula
def filter_efficiency():
    p = __p()
    __f_name = "data/filter/filter" + str(int(
        p.short_wavelength_limit.value * 1e8)).zfill(3) + ".json"
    __spec_list = pkg_resources.resource_filename('jasmine_toolkit', __f_name)
    return Efficiency.from_json(__spec_list)


earth_avoiding_angle = JasmineConstant(
    "earth_avoiding_angle", "earth_avoiding_angle",
    math.radians(25.7), "", 0.0
)

minimum_l = JasmineConstant(
    "minimum_l", "minimum_l",
    math.radians(-1.4), "", 0.0
)

maximum_l = JasmineConstant(
    "maximum_l", "maximum_l",
    math.radians(0.7), "", 0.0
)

minimum_b = JasmineConstant(
    "minimum_b", "minimum_b",
    math.radians(-0.6), "", 0.0
)

maximum_b = JasmineConstant(
    "maximum_b", "maximum_b",
    math.radians(0.6), "", 0.0
)


@constant_formula
def effective_focal_length():
    p = __p()
    return p.f_number * p.effective_pupil_diameter


def __weighted_mean(p, efficiency):
    wave_ref = np.linspace(p.short_wavelength_limit.value * 1e6,
                           p.long_wavelength_limit.value * 1e6, 1000)
    weight = np.ones(1000)
    warnings.warn('unit is lost.')
    return efficiency.weighted_mean(wave_ref, weight)


@constant_formula
def average_filter_efficiency():
    p = __p()
    return __weighted_mean(p, p.filter_efficiency)


@constant_formula
def average_telescope_throughput():
    p = __p()
    return __weighted_mean(p, p.optics_efficiency)


@constant_formula
def average_quantum_efficiency():
    p = __p()
    return __weighted_mean(p, p.quantum_efficiency)


@constant_formula
def total_efficiency():
    p = __p()
    return p.average_telescope_throughput \
           * p.average_filter_efficiency \
           * p.average_quantum_efficiency   # noqa


@constant_formula
def detector_format_x():
    p = __p()
    return p.n_row_ch - p.n_ref_pix_top - p.n_ref_pix_bottom


@constant_formula
def detector_format_y():
    p = __p()
    return p.n_col_ch * p.n_ch - p.n_ref_pix_left - p.n_ref_pix_right


@constant_formula
def orbital_period():
    p = __p()
    return 2 * math.pi * math.pow(
        p.EQUATORIAL_EARTH_RADIUS + p.orbital_altitude,
        1.5) / math.sqrt(
        p.CONST_OF_GRAVITATION * p.EARTH_MASS)


@constant_formula
def earth_mu():
    p = __p()
    return p.CONST_OF_GRAVITATION * p.EARTH_MASS


@constant_formula
def earth_c1():
    p = __p()
    return -3 * math.pi * p.EARTH_J2 * math.pow(
        p.EQUATORIAL_EARTH_RADIUS / 1000, 2) \
        * p.ONE_YEAR * math.sqrt(
            p.earth_mu) / 2 / math.pi * 180 / math.pi / math.pow(10000, 1.5)


@constant_formula
def earth_c2():
    p = __p()
    return 360 / p.earth_c1


@constant_formula
def inclination():
    p = __p()
    return math.acos(p.earth_c2 * math.pow(
        (p.EQUATORIAL_EARTH_RADIUS + p.orbital_altitude) /
        1000, 3.5)
                     * math.pow(
        1 - p.orbital_eccentricity * p.orbital_eccentricity,
        2) * math.sqrt(1000))


@constant_formula
def c_pix():
    p = __p()
    return p.reference_wavelength * p.f_number / p.pixel_size


@constant_formula
def read_time():
    p = __p()
    return p.n_col_ch * p.n_row_ch / p.pixel_sampling_frequency
