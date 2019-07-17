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

        self.OptionParser.add_option("", "--simulation_mode",
                                     action="store", type="inkbool",
                                     dest="simulation_mode", default=True,
                                     help="Approximate circle and draw semicreases for simulation?")

        self.OptionParser.add_option("", "--simulation_approximation",
                                     action="store", type="int",
                                     dest="simulation_approximation", default=20,
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
        self.translate = (R, R)

        if not self.options.simulation_mode:
            inner_circles = []
            for i in range(1, rings):
                inner_circles.append(Path((0, 0), radius=r + i*dr, style='m' if i % 2 else 'v'))

            edges = [Path((0, 0), radius=R, style='e'),
                     Path((0, 0), radius=r, style='e')]

            self.path_tree = [inner_circles, edges]

        # append semicreases for simulation
        else:
            dtheta = pi / self.options.simulation_approximation
            s = sin(dtheta)
            c = cos(dtheta)

            # Edge
            paths = [Path([(c * R, -s * R), (R, 0), (c * R, s * R)], style='e'),
                     Path([(c * r, -s * r), (r, 0), (c * r, s * r)], style='e')]

            # MV circles
            for i in range(1, rings):
                r_i = r + i * dr
                paths.append(Path([(c * r_i, -s * r_i), (r_i, 0), (c * r_i, s * r_i)],
                                          style='m' if i % 2 else 'v'))

            # Semicreases
            top = []
            bottom = []
            for i in range(rings + 1):
                r_i = r + i*dr
                top.append((r_i*(1 + (i % 2)*(c-1)), -(i % 2)*s*r_i))
                bottom.append((r_i*(1 + (i % 2)*(c-1)), (i % 2)*s*r_i))
            paths = paths + [Path([(r, 0), (R, 0)], 's'),                       # straight line 1
                             Path([(r*c, r*s), (R*c, R*s)], 's', invert=True),  # straight line 2
                             Path(top, 's'),                                    # top half of semicrease pattern
                             Path(bottom, 's')]                                # bottom half of semicrease pattern

            all_paths = [paths]
            for i in range(1, self.options.simulation_approximation):
                all_paths.append(Path.list_rotate(all_paths[0], i*2*dtheta))

            self.path_tree = all_paths




# Main function, creates an instance of the Class and calls inkex.affect() to draw the origami on inkscape
if __name__ == '__main__':
    e = PleatCircular()  # remember to put the name of your Class here!
    e.affect()
