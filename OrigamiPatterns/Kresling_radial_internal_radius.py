#! /usr/bin/env python
# -*- coding: utf-8 -*-
from math import sin, asin, pi, ceil
import inkex

from Path import Path
from Pattern import Pattern
from Kresling import Kresling


class KreslingRadial(Kresling):
    
    def __init__(self):
        """ Constructor
        """
        Kresling.__init__(self)  # Must be called in order to parse common options

        self.OptionParser.add_option("", "--radial_ratio",
                                     action="store", type="float",
                                     dest="radial_ratio", default=0.5,
                                     help="Radial ratio")

        self.OptionParser.add_option("", "--internal_radius",
                                     action="store", type="float",
                                     dest="internal_radius", default=5.0,
                                     help="Internal Radius ratio")

        self.OptionParser.add_option("", "--minimize_external_radius",
                                     action="store", type="inkbool", 
                                     dest="minimize_external_radius", default=False,
                                     help="Maximize radial ratio and minimize external radius")
        
    def generate_path_tree(self):
        """ Convert radial to angular ratio, then call regular Kresling constructor
        """
        # convert options from radial to angular ratio
        # if self.options.minimize_polygon:
        #     self.options.sides = max(3, int(ceil(2. / (1. - (4./pi)*asin(self.options.radial_ratio)))))
        
        max_radial_ratio = sin((pi/4)*(1. - 2./self.options.sides))
        if self.options.minimize_external_radius:
            self.options.radial_ratio = max_radial_ratio

        elif self.options.radial_ratio > max_radial_ratio:
            inkex.errormsg(_("For polygon of {} sides, the maximal radial ratio is = {}\n"
                             "Lower ratio, increase number of sides or select "
                             "\"Minimize polygon sides\" option.".format(self.options.sides, max_radial_ratio)))
            self.options.radial_ratio = max_radial_ratio

        self.options.angle_ratio = 1 - 2*self.options.sides*asin(self.options.radial_ratio)/((self.options.sides-2)*pi)
        self.options.radius = self.options.internal_radius / self.options.radial_ratio

        # inkex.debug('new = {}'.format(self.options.angle_ratio))
        Kresling.generate_path_tree(self)


if __name__ == '__main__':
    e = KreslingRadial()
    e.affect()
