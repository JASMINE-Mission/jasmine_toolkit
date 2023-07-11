import astropy.units.quantity
from jasmine_toolkit.utils import parameter as p
from jasmine_toolkit.utils.constants.jasmine_constant import JasmineConstant

p.ready()
v_list = [
# te;escp@e
    p.effective_pupil_diameter,
    ["central obscuration ratio", p.central_obscuration_ratio],
    ["F number", p.f_number],
    p.long_wavelength_limit,
    p.short_wavelength_limit,
    p.reference_wavelength,
    p.spider_thickness,
    ["spider type", p.spider_type],
    ["effective focal length", p.effective_focal_length, 1],
#    p.filter_efficiency, # return value is Efficiency object
    ["average telescope throughput", p.average_telescope_throughput, 1], # phy unit exists?
    ["average filter efficiency", p.average_filter_efficiency, 1], # why unit exists?

    # detector
    p.pixel_size,
#    p.dark_current,  # unit pix is not acceptable
#    p.background_photon_flux,  # unit pix is not acceptable
    p.detector_separation_x,
    p.detector_separation_y,
    ["full well electron", p.full_well_electron],
    ["number of detector in x direction", p.num_detector_x],
    ["number of detector in y direction", p.num_detector_y],
    ["number of columns in a channel", p.n_col_ch],
    ["number of rows in a channel", p.n_row_ch],
    ["number of channels", p.n_ch],
    ["number of the reference pixels in left", p.n_ref_pix_left],
    ["number of the reference pixels in right", p.n_ref_pix_right],
    ["number of the reference pixels in top", p.n_ref_pix_top],
    ["number of the reference pixels in bottom", p.n_ref_pix_bottom],
    ["average quantum efficiency", p.average_quantum_efficiency, 1],  # why unit exists?
    ["detector format in x direction", p.detector_format_x, 1],
    ["detector format in x direction", p.detector_format_y, 1],
    # detector electronics
    p.pixel_sampling_frequency,
    ["read out noise", p.read_out_noise],
    ["read time", p.read_time, 1],

    # operation
    ## orbit
    p.orbital_altitude,
    p.ltan,
    ["orbital eccentricity", p.orbital_eccentricity],
    ["orbital period", p.orbital_period, 1],
    ["inclination", p.inclination, 1],
    ## AOCS
    p.maneuver_time,
    p.large_maneuver_time,
    p.attitude_control_error_mas,
    ## observation
    p.exposure_time,
    p.earth_avoiding_angle,
    ["window size in x direction", p.window_size_x],
    ["window size in y direction", p.window_size_y],
    ## Science region
    p.minimum_l,
    p.maximum_l,
    p.minimum_b,
    p.maximum_b,
    ["saturation magnitude", p.saturation_magnitude],
    ["standard magnitude", p.standard_magnitude],
    ["faint end magnitude", p.faint_end_magnitude],
    # other parameters
    ["cell pix", p.cell_pix],
    ["Use M flag", p.use_M_flag],
    ["total efficiency", p.total_efficiency, 1],  # why unit exists?
    ["earth J2", p.EARTH_J2],
    ["parameter C", p.c_pix, 1],
    ["earth mu", p.earth_mu, 1],
    ["earth C1", p.earth_c1, 1],
    ["earth C2", p.earth_c2, 1],
    p.EARTH_MASS,
    p.CONST_OF_GRAVITATION,
    p.EQUATORIAL_EARTH_RADIUS,
    p.POLAR_EARTH_RADIUS,
    p.ONE_YEAR,
]

def write_to_file(filename: str):
    fp = open(filename, "w", encoding="utf-8")
    fp.write("Parameter List\n^Name ^Value ^Units ^Comments^\n")
    for i in range(len(v_list)):
        if isinstance(v_list[i], JasmineConstant):
            fp.write("|" + str(v_list[i].name) + "|" + str(v_list[i].value)
                     + "|" + str(v_list[i].unit) + "|"
                     + str(v_list[i].reference) + "|\n")
        elif isinstance(v_list[i], list):
            if isinstance(v_list[i][1], astropy.units.quantity.Quantity):
                fp.write("|" + v_list[i][0] + "|" + str(v_list[i][1].value)
                         + "|" + str(v_list[i][1].unit) + "|")
            else:
                fp.write("|" + v_list[i][0] + "|" + str(v_list[i][1]) + "| |")
            if len(v_list[i]) == 3:
                fp.write("induced")
            fp.write("|\n")
    fp.close()

if __name__ == '__main__':
    write_to_file("tmp.txt")
