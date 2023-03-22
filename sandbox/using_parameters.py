#!/usr/bin/env
import astropy.units as u
import numpy as np
import jasmine_toolkit.parameters as p


def double(x):
    print(x * 2)


print('\n### show the default parameters ###')
p.print_parameters()

print('\n### update `naxis1` to 1000 pix ###')
p.naxis1 = 1000 * u.pixel

print('### update `naxis2` to 900 pix ###')
p.naxis2.update(900, unit='pix')

print('### update `pixel_scale` to 0.009 mm')
p.pixel_scale.update(0.009 * u.mm)

print('### update `tel_efficiency` to 0.009 mm')
eff = np.array([
    (1, 0),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 0),
    (6, 0),
], dtype=[('walvelength', 'f8'), ('flux', 'f8')])
p.tel_efficiency = u.quantity.Quantity(eff, u.Unit('um, 1'))

print('\n### show the updated parameters ###')
p.print_parameters()

print('\n### calculate using parameters ###')
with p.finalized_context():
    double(p.naxis1)
    double(p.naxis2)
    double(p.pixel_scale.to(u.km))
    double(p.field_of_view)
