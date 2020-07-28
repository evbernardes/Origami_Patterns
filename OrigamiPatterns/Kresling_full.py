#! /usr/bin/env python
# -*- coding: utf-8 -*-
from math import sin, cos, asin, pi, ceil
import inkex

from Path import Path
from Pattern import Pattern
from Kresling import Kresling


class KreslingRadial(Kresling):
    
    def __init__(self):
        """ Constructor
        """
        Kresling.__init__(self)  # Must be called in order to parse common options

        self.add_argument('--measure_value',
                         action="store", type="float",
                         dest="measure_value", default=10.0,
                         help="Length")

        self.add_argument('--measure_type',
                         action="store", type="string",
                         dest="measure_type", default=60,
                         help="Type of length")

        self.add_argument('--parameter_type',
                         action="store", type="string",
                         dest="parameter_type", default=60,
                         help="Type of parameter")

        self.add_argument('--radial_ratio',
                         action="store", type="float",
                         dest="radial_ratio", default=0.5,
                         help="Radial ratio")

        self.add_argument('--angle_ratio',
                         action="store", type="float",
                         dest="angle_ratio", default=0.5,
                         help="Anle ratio")

        self.add_argument('--phi',
                         action="store", type="float",
                         dest="phi", default=45,
                         help="phi")
        
    def generate_path_tree(self):
        """ Convert radial to angular ratio, then call regular Kresling constructor
        """
        n = self.options.sides
        theta = pi*(n-2)/(2*n)   
        # define ratio parameter
        parameter = self.options.parameter_type
        if parameter == 'radial_ratio':
            radial_ratio = self.options.radial_ratio
            max_radial_ratio = sin((pi/4)*(1. - 2./n))
            if radial_ratio > max_radial_ratio:
                inkex.errormsg(_("For polygon of {} sides, the maximal radial ratio is = {}".format(n, max_radial_ratio)))
                radial_ratio = max_radial_ratio
            angle_ratio = 1 - 2*n*asin(radial_ratio)/((n-2)*pi)
        elif parameter == 'phi':
            phi = self.options.phi
            angle_min = 45. * (1 - 2. / n)
            angle_max = 2 * angle_min
            if phi < angle_min:
                inkex.errormsg(_(
                    "For polygon of {} sides, phi must be between {} and {} degrees, \nsetting phi = {}\n".format(
                        n, angle_min, angle_max, angle_min)))
                phi = angle_min
            elif phi > angle_max:
                inkex.errormsg(_(
                    "For polygon of {} sides, phi must be between {} and {} degrees, \nsetting phi = {}\n".format(
                        n, angle_min, angle_max, angle_max)))
                phi = angle_max
            angle_ratio = phi * n / (90. * (n - 2.))
        self.options.angle_ratio = angle_ratio

        # define some length
        mtype = self.options.measure_type
        mvalue = self.options.measure_value
        if mtype == 'a':
            radius = 0.5*mvalue / (sin(pi/n))
        elif mtype == 'l':
            radius = 0.5*mvalue/cos(theta*(1-angle_ratio))
        elif mtype == 'radius_external':
            radius = mvalue
        elif mtype == 'radius_internal':
            radius = mvalue/(sin(theta*(1-angle_ratio)))
        elif mtype == 'diameter_external':
            radius = 0.5*mvalue
        elif mtype == 'diameter_internal':
            radius = 0.5*mvalue/sin(theta*(1-angle_ratio))

        # inkex.errormsg(_("Value = {}, Mode = {}, Radius = {}".format(mvalue, mtype, radius)))

        if self.options.pattern == 'mirrowed':
            self.options.mirror_cells = True
        else:
            self.options.mirror_cells = False
        self.options.radius = radius

        Kresling.generate_path_tree(self)


if __name__ == '__main__':
    e = KreslingRadial()
    e.draw()
