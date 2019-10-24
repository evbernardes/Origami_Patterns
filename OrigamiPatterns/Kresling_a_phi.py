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

        self.OptionParser.add_option("", "--a",
                                     action="store", type="float", 
                                     dest="a", default=10.0,
                                     help="Length of side of polygon")

        self.OptionParser.add_option("", "--phi",
                                     action="store", type="float",
                                     dest="phi", default=60,
                                     help="Angle between a and l (phi)")
        
    def generate_path_tree(self):
        """ Convert radial to angular ratio, then call regular Kresling constructor
        """
        phi = self.options.phi

        angle_min = 45. * (1 - 2. / self.options.sides)
        angle_max = 2 * angle_min

        if phi < angle_min:
            inkex.errormsg(_("For polygon of {} sides, phi must be between {} and {} degrees, \nsetting phi = {}\n".format(self.options.sides, angle_min, angle_max, angle_min)))
            phi = angle_min
        elif phi > angle_max:
            inkex.errormsg(_("For polygon of {} sides, phi must be between {} and {} degrees, \nsetting phi = {}\n".format(self.options.sides, angle_min, angle_max, angle_max)))
            phi = angle_max

        self.options.angle_ratio = phi * self.options.sides / (90. * (self.options.sides-2.))
        self.options.radius = self.options.a / (2 * sin(pi/self.options.sides))

        # inkex.debug('new = {}'.format(self.options.angle_ratio))
        Kresling.generate_path_tree(self)


if __name__ == '__main__':
    e = KreslingRadial()
    e.affect()
