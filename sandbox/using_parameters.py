#!/usr/bin/env
import astropy.units as u
import jasmine_toolkit.parameters as p


def double(x):
    print(x * 2)


print('### show the default parameters ###')
p.print_parameters()

print('### update `naxis1` to 1000 pix ###')
p.naxis1 = 1000 * u.pixel

print('### update `naxis2` to 900 pix ###')
p.naxis2.update(900, unit='pixel')

print('### update `pixel_scale` to 0.009 mm')
p.pixel_scale.update(0.009 * u.mm)

print('### show the updated parameters ###')
p.print_parameters()


with p.finalized_context():
    double(p.naxis1)
    double(p.naxis2)
    double(p.pixel_scale.to(u.km))
