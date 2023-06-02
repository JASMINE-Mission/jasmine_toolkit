from astropy.coordinates import SkyCoord
import astropy.units as u
import csv


class AstrometricCatalogue:
    def __init__(self, catalogue_entries: list[CatalogueEntry] = []):
        """Constructor

        Args:
            catalogue_entries: list of CatalogueEntry
        """
        self.__stellar_ids = []
        self.__parallaxes = []
        self.__proper_motion_beta = []
        self.__proper_motion_lambda = []
        self.__beta0 = []
        self.__lambda0 = []

    def get_catalogue(self) -> list[CatalogueEntry]:
        """

        Returns: array of CatalogueEntry

        """
        return self.__catalogue_entries

    def save(self, file_name: str):
        with open(file_name, 'w', newline='') as data_file:
            write = csv.writer(data_file)
            for e in self.__catalogue_entries:
                write.writerow([e.stellar_id, e.coord.icrs.ra.deg, e.coord.icrs.dec.deg,
                                e.coord.icrs.pm_ra_cosdec.to_value(u.mas / u.yr),
                                e.coord.icrs.pm_dec.to_value(u.mas / u.yr),
                                e.coord.distance.to_value(u.pc), e.coord.obstime, e.mag])

    @staticmethod
    def load(file_name: str):
        tmp = []
        file = open(file_name, 'r', newline='')
        f = csv.reader(file, delimiter=',')
        for row in f:
            tmp.append(CatalogueEntry(stellar_id=int(row[0]),
                                      coord=SkyCoord(ra=float(row[1]), dec=float(row[2]), unit=('deg', 'deg'),
                                                     pm_ra_cosdec=float(row[3]) * u.mas / u.yr,
                                                     pm_dec=float(row[4]) * u.mas / u.yr, distance=float(row[5]) * u.pc,
                                                     obstime=row[6], frame='icrs'), mag=float(row[7])))
        return AstrometricCatalogue(tmp)
