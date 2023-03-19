#!/usr/bin/env
import astropy.units as u
import jasmine_toolkit.parameters as p


p.print_parameters()

p.naxis1 = 1000 * u.pixel

p.print_parameters()
