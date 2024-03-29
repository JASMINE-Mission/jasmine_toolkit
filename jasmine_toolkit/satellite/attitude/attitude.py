import math
import random
import astropy
import astropy.units as u
from astropy.coordinates import get_sun, SkyCoord
from astropy.time import Time
from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom


class Attitude:
    def __init__(self, mode: EnumPointingFreedom):
        self.__mode = mode

    def get_position_angle(self, pointing: SkyCoord, time: Time) -> float:
        """
        Calculate position angle in degree. Position angle is defined as the
        direction of north and direction of +x direction (direction of sun
        shield) in satellite.
        Args:
            pointing: Telescope pointing direction on the celestial sphere in
              astropy.coordinates.SkyCoord.
            time: Observation time in astropy.time.Time.

        Returns:
            position angle in radian.
        """
        # TODO all these calculation should be done via attitude quaternion
        # get solar direction
        sun = get_sun(time)
        # calculate pointing direction in right ascension and declination
        dec = pointing.icrs.dec.to('rad').value
        ra = pointing.icrs.ra.to('rad').value
        # calculate north perpendicular direction ra_np and dec_np to the
        # pointing direction
        np = pointing.directional_offset_by(
            pointing.position_angle(SkyCoord(0., 90., unit='deg')),
            90.0 * u.deg).icrs
        dec_np = np.dec.to('rad').value
        ra_np = np.ra.to('rad').value
        if self.__mode == EnumPointingFreedom.POINTING_RANDOM:
            dec_np = dec_np + 0.34 * (random.random() - 0.5)
        # TODO factor 0.34 which means 20 degrees in radian should be variable
        #  parameter
        # return position angle from satellite north pole to sun
        return astropy.coordinates.position_angle(ra_np * u.rad, dec_np * u.rad,
                                                  sun.ra, sun.dec).to('rad') \
            .value
