#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from math import pi, sin, cos

from Path import Path
from Pattern import Pattern


# Select name of class, inherits from Pattern
# TODO:
# 1) Implement __init__ method to get all custom options and then call Pattern's __init__
# 2) Implement generate_path_tree to define all of the desired strokes


class PleatCircular(Pattern):

    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        # save all custom parameters defined on .inx file
        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="pleat_circular",
                                     help="Origami pattern")

        self.OptionParser.add_option("", "--radius",
                                     action="store", type="float",
                                     dest="radius", default=55.0,
                                     help="Radius of circle")

        self.OptionParser.add_option("", "--ratio",
                                     action="store", type="float",
                                     dest="ratio", default=0.4,
                                     help="Opening ratio")

        self.OptionParser.add_option("", "--rings",
                                     action="store", type="int",
                                     dest="rings", default=15,
                                     help="Number of rings")

        self.OptionParser.add_option("", "--semicreases_bool",
                                     action="store", type="inkbool",
                                     dest="semicreases_bool", default=True,
                                     help="Draw semicreases for simulator?")

        self.OptionParser.add_option("", "--semicreases_number",
                                     action="store", type="int",
                                     dest="semicreases_number", default=20,
                                     help="Semicreases division")

    def generate_path_tree(self):
        """ Specialized path generation for your origami pattern
        """
        # retrieve saved parameters
        unit_factor = self.calc_unit_factor()
        R = self.options.radius * unit_factor
        ratio = self.options.ratio
        r = R * ratio
        rings = self.options.rings
        dr = (1.-ratio)*R/rings

        inner_circles = []
        for i in range(1, rings):
            inner_circles.append(Path((0, 0), radius=r + i*dr, style='m' if i % 2 else 'v'))

        edges = [Path((0, 0), radius=R, style='e'),
                 Path((0, 0), radius=r, style='e')]

        self.translate = (R, R)
        self.path_tree = [inner_circles, edges]

        # append semicreases for simulation
        if self.options.semicreases_bool:
            top = []
            bottom = []
            dtheta = pi / self.options.semicreases_number
            s = sin(dtheta)
            c = cos(dtheta)
            for i in range(rings + 1):
                r_i = r + i*dr
                top.append((r_i*(1 + (i % 2)*(c-1)), -(i % 2)*s*r_i))
                bottom.append((r_i*(1 + (i % 2)*(c-1)), (i % 2)*s*r_i))
            semicreases = [[Path([(r, 0), (R, 0)], 's'),
                           Path([(r*c, r*s), (R*c, R*s)], 's', invert=True),
                           Path(top, 's'),
                           Path(bottom, 's')]]

            for i in range(1, self.options.semicreases_number):
                semicreases.append(Path.list_rotate(semicreases[0], i*2*dtheta))
            self.path_tree.append(semicreases)




# Main function, creates an instance of the Class and calls inkex.affect() to draw the origami on inkscape
if __name__ == '__main__':
    e = PleatCircular()  # remember to put the name of your Class here!
    e.affect()
