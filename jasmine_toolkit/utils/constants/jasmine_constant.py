from astropy.constants import Constant
import pkg_resources
from jasmine_toolkit.datamodel.efficiency import Efficiency


class JasmineConstant(Constant):
    # TODO 規格の切り返したい場合は、このクラスから切り離した方が良いです
    # 規格の切り替えはこの辺で行ってます
    # see https://github.com/astropy/astropy/blob/main/astropy/constants/config.py
    default_reference = "JASMINE"
    _registry = {}
    _has_incompatible_units = set()


EARTH_MASS = JasmineConstant(
    "EARTH_MASS", "Earth mass", 5.9724E24, "kg", 0.0
)

maneuver_time = JasmineConstant(
    "maneuver_time", "maneuver_time", 115, "s", 0.0
)

long_wavelength_limit = JasmineConstant(
    "long_wavelength_limit", "long_wavelength_limit", 1.6e-6, "m", 0.0
)

short_wavelength_limit = JasmineConstant(
    "short_wavelength_limit", "short_wavelength_limit", 1.0e-6, "m", 0.0
)

__f_name = "data/filter/filter" + str(int(
    short_wavelength_limit.value * 1e8)).zfill(3) + ".json"
__spec_list = pkg_resources.resource_filename('jasmine_toolkit', __f_name)

filter_efficiency = Efficiency.from_json(__spec_list)