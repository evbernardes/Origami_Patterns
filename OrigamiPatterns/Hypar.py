#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from math import pi, tan, sqrt, sin, cos

import inkex

from Path import Path
from Pattern import Pattern


class Hypar(Pattern):

    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        # save all custom parameters defined on .inx file
        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="template1",
                                     help="Origami pattern")

        self.OptionParser.add_option("", "--radius",
                                     action="store", type="float",
                                     dest="radius", default=10.0,
                                     help="Radius of tower (mm)")

        self.OptionParser.add_option("", "--sides",
                                     action="store", type="int",
                                     dest="sides", default=4,
                                     help="Number of polygon sides")

        self.OptionParser.add_option("", "--rings",
                                     action="store", type="int",
                                     dest="rings", default=7,
                                     help="Number of rings")

        self.OptionParser.add_option("", "--simplify_center",
                                     action="store", type="inkbool",
                                     dest="simplify_center", default=0,
                                     help="Simplify center")

    def generate_path_tree(self):
        """ Specialized path generation for your origami pattern
        """
        # retrieve saved parameters
        unit_factor = self.calc_unit_factor()
        pattern = self.options.pattern
        radius = self.options.radius * unit_factor
        sides = self.options.sides
        rings = self.options.rings
        simplify_center = self.options.simplify_center
        sin_ = sin(pi / float(sides))
        a = radius*sin_  # half of length of polygon side
        H = radius*sqrt(1 - sin_**2)

        # create diagonals
        diagonals = []
        for i in range(sides):
            p1 = (0, 0)
            p2 = (radius * cos((1 + i * 2) * pi / sides), radius * sin((1 + i * 2) * pi / sides))
            diagonals.append(Path([p1, p2], 'u'))

        # create generic closed ring
        closed_ring = Path([p.points[-1] for p in diagonals], 'm', closed=True)

        # separate generic closed ring to create edges
        edges = Path.generate_separated_paths(closed_ring.points, 'e', closed=True)

        # scale generic closed ring to create inner rings
        inner_rings = []
        for i in range(rings + 1):
            inner_rings.append(closed_ring * (float(i)/(rings+1)))
            if i % 2:
                inner_rings[i].style = 'v'

        # # create points for zig zag pattern
        zig_zags = []
        if pattern != "classic":
            zig_zag = []
            for i in range(1, rings + 1):
                y_out = a * ((i + 1.) / (rings + 1.))
                y_in = a * (float(i) / (rings + 1.))
                x_out = H * (i + 1.) / (rings + 1.)
                x_in = H * float(i) / (rings + 1.)

                if pattern == "alternate_asymmetric" and i%2:
                    zig_zag.append(Path([(x_in, -y_in), (x_out, y_out), ], style='u'))
                else:
                    zig_zag.append(Path([(x_in, y_in), (x_out, -y_out)], style='u'))
                # inkex.debug(zig_zag[i].points)

            # reflect zig zag pattern to create all sides
            zig_zags.append(zig_zag)
            for i in range(sides - 1):
                zig_zags.append(Path.list_reflect(zig_zags[i], *diagonals[i].points))

        # modify center if needed
        if simplify_center:
            for i in range(sides):
                if i % 2 == 0:
                    p2 = diagonals[i].points[1]
                    p1 = (1./(rings+1) * p2[0], 1./(rings+1) * p2[1])
                    diagonals[i] = Path([p1, p2], 'u')

        self.translate = (radius, radius)
        self.path_tree = [diagonals, zig_zags, inner_rings, edges]

# Main function, creates an instance of the Class and calls inkex.affect() to draw the origami on inkscape
if __name__ == '__main__':
    e = Hypar()  # remember to put the name of your Class here!
    e.affect()
