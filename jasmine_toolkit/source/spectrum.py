#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Stellar spectrum '''

from synphot.spectrum import SourceSpectrum, Empirical1D
from functools import lru_cache

from ..extinction import NL20


__spectral_types = {
    'O5V': 'uko5v',
    'O8III': 'uko8iii',
    'O9V': 'uko9v',
    'B0I': 'ukb0i',
    'B0V': 'ukb0v',
    'B1I': 'ukb1i',
    'B1III': 'ukb12iii',
    'B1V': 'ukb1v',
    'B2II': 'ukb2ii',
    'B2III': 'ukb12iii',
    'B3I': 'ukb3i',
    'B3III': 'ukb3iii',
    'B3V': 'ukb3v',
    'B5I': 'ukb5i',
    'B5II': 'ukb5ii',
    'B5III': 'ukb5iii',
    'B5V': 'ukb57v',
    'B6V': 'ukb57v',
    'B7V': 'ukb57v',
    'B8I': 'ukb8i',
    'B9III': 'ukb9iii',
    'B9V': 'ukb9v',
    'A0I': 'uka0i',
    'A0III': 'uka0iii',
    'A0IV': 'uka0iv_new',
    'A0V': 'uka0v',
    'A2I': 'uka2i',
    'A2V': 'uka2v',
    'A3III': 'uka3iii',
    'A3V': 'uka3v',
    'A4IV': 'uka47iv',
    'A5III': 'uka5iii',
    'A5IV': 'uka47iv',
    'A5V': 'uka5v',
    'A6IV': 'uka47iv',
    'A7III': 'uka7iii',
    'A7IV': 'uka47iv',
    'A7V': 'uka7v',
    'F0I': 'ukf0i',
    'F0II': 'ukf0ii',
    'F0III': 'ukf0iii',
    'F0IV': 'ukf02iv',
    'F0V': 'ukf0v',
    'F1IV': 'ukf12iv',
    'F2II': 'ukf2ii',
    'F2III': 'ukf2iii',
    'F2IV': 'ukf02iv',
    'F2V': 'ukf2v',
    'F5III': 'ukf5iii',
    'F5IV': 'ukf5iv',
    'F5V': 'ukf5v',
    'F6V': 'ukf6v',
    'F8I': 'ukf8i',
    'F8iv': 'ukf8iv',
    'F8V': 'ukf8v',
    'G0I': 'ukg0i',
    'G0III': 'ukg0iii',
    'G0IV': 'ukg0iv_new',
    'G0V': 'ukg0v',
    'G2I': 'ukg2i',
    'G2IV': 'ukg2iv_new',
    'G2V': 'ukg2v',
    'G5I': 'ukg5i',
    'G5II': 'ukg5ii',
    'G5III': 'ukg5iii',
    'G5IV': 'ukg5iv_new',
    'G5V': 'ukg5v',
    'G8I': 'ukg8i',
    'G8III': 'ukg8iii',
    'G8IV': 'ukg8iv',
    'G8V': 'ukg8v',
    'K0II': 'ukk01ii',
    'K0III': 'ukk0iii',
    'K0IV': 'ukk0iv_new',
    'K0V': 'ukk0v',
    'K1II': 'ukk01ii',
    'K1III': 'ukk1iii',
    'K1IV': 'ukk1iv_new',
    'K2I': 'ukk2i',
    'K2III': 'ukk2iii',
    'K2V': 'ukk2v',
    'K3I': 'ukk3i',
    'K3II': 'ukk34ii',
    'K3III': 'ukk3iii',
    'K3IV': 'ukk3iv',
    'K3V': 'ukk3v',
    'K4I': 'ukk4i',
    'K4II': 'ukk34ii',
    'K4III': 'ukk4iii',
    'K4V': 'ukk4v_new',
    'K5III': 'ukk5iii',
    'K5V': 'ukk5v',
    'K7V': 'ukk7v',
    'M0III': 'ukm0iii',
    'M0V': 'ukm0v',
    'M1III': 'ukm1iii',
    'M1V': 'ukm1v',
    'M2I': 'ukm2i',
    'M2III': 'ukm2iii',
    'M3II': 'ukm3ii',
    'M3III': 'ukm3iii',
    'M3V': 'ukm3v',
    'M4III': 'ukm4iii',
    'M4V': 'ukm4v_new',
    'M5III': 'ukm5iii',
    'M5V': 'ukm5v',
    'M6III': 'ukm6iii',
    'M6V': 'ukm6v',
    'M7III': 'ukm7iii',
    'M8III': 'ukm8iii',
    'M9III': 'ukm9iii',
    'M10III': 'ukm10iii',
}


def __template(name):
    ''' URL template to the ESO IR spectral library '''
    return (
        'ftp://ftp.eso.org/web/sci/observing/tools'
        f'/standards/IR_spectral_library/{name}.dat.gz')


@lru_cache(maxsize=32)
def __fetch_spectrum(spectral_type):
    ''' Fetch a stellar spectrum from the ESO IR spectral library. '''

    if spectral_type.upper() not in __spectral_types:
        raise ValueError(f'Unknown spectral type: {spectral_type}')

    name = __spectral_types[spectral_type.upper()]
    url = __template(name)
    return SourceSpectrum.from_file(url)


def fetch_spectrum(spectral_type, Av=0.0, extinction_model=None):
    ''' Fetch a stellar spectrum from the ESO IR spectral library.

    Arguments:
        spectral_type: str
            The spectral type of the star (e.g., 'G2V').

        Av: float
            The amount of visual extinction to apply to the spectrum.
            Default is 0.0 (no extinction).

        extinction_model: Extinction model
            The extinction model to use for applying extinction.
            A model should have an `extinguish` method that takes
            a wavelength array and an `Av` parameter.
            If not specified, the NL20 model is used.
    '''

    spc = __fetch_spectrum(spectral_type)

    if extinction_model is None:
        extinction_model = NL20()

    waveset = spc.waveset
    flux = spc(waveset) * extinction_model.extinguish(waveset, Av=Av)
    meta = spc.meta.copy()
    meta.update({
        'spectral_type': spectral_type.upper(),
        'Av': Av,
        'extinction_model': extinction_model.__class__.__name__,
    })

    return SourceSpectrum(
        Empirical1D,
        points=waveset,
        lookup_table=flux,
        meta=meta
    )
