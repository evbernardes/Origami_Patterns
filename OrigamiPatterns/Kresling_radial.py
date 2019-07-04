#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import inkex

from Path import Path
from Pattern import Pattern
from Kresling import Kresling


class Kresling_radial(Kresling):
    
    def __init__(self):
        ''' Constructor
        '''
        Kresling.__init__(self)  # Must be called in order to parse common options

        self.OptionParser.add_option("", "--radial_ratio",
                                     action="store", type="float", 
                                     dest="radial_ratio", default=0.5,
                                     help="Radial ratio")

        self.OptionParser.add_option("", "--minimize_polygon",
                                     action="store", type="inkbool", 
                                     dest="minimize_polygon", default=False,
                                     help="Minimize polygon for radial ratio")
        
    def generate_path_tree(self):
        ''' Convert radial to angular ratio, then call regular Kresling constructor
        '''
        # convert options from radial to angular ratio
        if self.options.minimize_polygon == True:
            self.options.sides = max(3,int(math.ceil(2. / (1. - (4./math.pi)*math.asin(self.options.radial_ratio)))))
        
        max_radial_ratio = math.sin((math.pi/4)*(1. - 2./self.options.sides))
        if (self.options.radial_ratio > max_radial_ratio):
            inkex.errormsg(_("For polygon of {} sides, the maximal radial ratio is = {}\n"
                "Lower ratio, increase number of sides or select "
                "\"Minimize polygon sides\" option.".format(self.options.sides,max_radial_ratio)))
            self.options.radial_ratio = max_radial_ratio
        self.options.angle_ratio = 1 - 2*self.options.sides*math.asin(self.options.radial_ratio)/((self.options.sides-2)*math.pi)

        # inkex.debug('new = {}'.format(self.options.angle_ratio))
        Kresling.generate_path_tree(self)

if __name__ == '__main__':
    e = Kresling_radial()
    e.affect()