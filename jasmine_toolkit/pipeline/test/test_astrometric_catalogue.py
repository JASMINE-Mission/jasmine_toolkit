import csv
import pytest
from astropy.coordinates import SkyCoord
import astropy.units as u
from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.catalog_entry import CatalogueEntry
from test_pipeline import get_tests_file_name
from test_tools.test_file_utils import get_temp_file

@pytest.fixture
def csv_line():
    a = AstrometricCatalogue([
        CatalogueEntry(1,
                       SkyCoord(l=0., b=0., unit=('rad', 'rad'), frame='galactic', obstime='2000-01-01 00:00:00.0',
                                distance=1.0 * u.pc, pm_l_cosb=10 * u.mas / u.yr, pm_b=10 * u.mas / u.yr),
                       12.5),
    ])
    tmp_file = get_temp_file()
    f_name = str(tmp_file)
    a.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    return next(iter(f))


def test_save1(csv_line):
    assert int(csv_line[0]) == 1
    assert abs(float(csv_line[1]) - 266.4049882865447) < 0.01
    assert abs(float(csv_line[2]) + 28.936177761791473) < 0.01
    assert abs(float(csv_line[3]) + 3.325090692327255) < 0.01


def test_save2(csv_line):
    assert abs(float(csv_line[4]) - 13.745681936077188) < 0.01
    assert abs(float(csv_line[5]) - 1.0) < 0.1
    assert csv_line[6] == '2000-01-01 00:00:00.000'
    assert abs(float(csv_line[7]) - 12.5) < 0.1


@pytest.fixture
def loaded_value():
    f_name = str(get_tests_file_name('astrometric_catalogue.csv'))
    a = AstrometricCatalogue.load(f_name)
    return a.get_catalogue()


def test_load1(loaded_value):
    assert loaded_value[0].stellar_id == 1
    assert abs(loaded_value[0].ra - 266.4049882865447) < 0.01
    assert abs(loaded_value[0].dec + 28.936177761791473) < 0.01
    assert abs(loaded_value[0].pm_ra_cosdec + 3.325090692327255) < 0.01


def test_load2(loaded_value):
    assert abs(loaded_value[0].pm_dec - 13.745681936077188) < 0.01
    assert abs(loaded_value[0].distance - 1.0) < 0.1
    assert str(loaded_value[0].coord.obstime) == '2000-01-01 00:00:00.000'
    assert abs(loaded_value[0].mag - 12.5) < 0.1
