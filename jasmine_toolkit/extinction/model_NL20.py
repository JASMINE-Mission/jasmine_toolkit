#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This module provides an extinction model for stars around the galactic center
region, based on the extinction law estimated by Nogueras-Lara et al. (2020).
The model modifies the Fitzpatrick et al. (2019) extinction law to better fit
the JHKs extinction law measured in the GALACTICNUCLEUS survey.

Classes:
    NL20: A modified extinction model for the galactic center region.

References:
    [1] Nogueras-Lara et al. (2020):
        https://ui.adsabs.harvard.edu/abs/2020A%26A...641A.141N/abstract
    [2] Fitzpatrick et al. (2019):
        https://ui.adsabs.harvard.edu/abs/2019ApJ...886..108F/abstract
'''

from dust_extinction.parameter_averages import F19
import numpy as np
import astropy.units as u


class NL20:
    ''' Extinction model NL20

    Stars around the galactic center region are strongly affected by dust
    extinction. The extinction law around the galactic center was estimated
    by [Nogueras-Lara et al. (2020)][1] based on the GALACTICNUCLEUS survey.
    The estimated extinction law is much steeper than a typical extinction
    law calibrated in several sight lines in the Milky way and local
    galaxies. Thus, we slightly modified the extinction model provided by
    [Fitzpatrick et al. (2019)][2] to fit the JHKs extinction law measured
    by Nogueras-Lara et al. (2020). The modified extinction curve is
    illustrated below.

    [1]: https://ui.adsabs.harvard.edu/abs/2020A%26A...641A.141N/abstract
    [2]: https://ui.adsabs.harvard.edu/abs/2019ApJ...886..108F/abstract
    '''
    lambda_j = 1.235 * u.um
    lambda_h = 1.662 * u.um

    def __init__(self, pp=-0.5, original_Rv=3.1):
        self.__pp = pp
        self.__Rv = original_Rv
        self.__anchor = 5500 * u.angstrom

    @property
    def __model(self):
        return F19(Rv=self.__Rv)

    def __factor(self, l):
        return (l / self.__anchor)**self.__pp

    def extinguish(self, wavelength, Av):
        return self.__model.extinguish(wavelength, Av) \
            ** self.__factor(wavelength)

    def extinction(self, wavelength, Av):
        return -2.5 * np.log10(self.extinguish(wavelength, Av))
