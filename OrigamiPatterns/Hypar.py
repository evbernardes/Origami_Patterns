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
        pattern = self.options.pattern
        radius = self.options.radius
        sides = self.options.sides
        rings = self.options.rings
        simplify_center = self.options.simplify_center
        sin_ = sin(pi / float(sides))
        H = radius*sqrt(1 - sin_**2)

        # create diagonals
        diagonals = []
        for i in range(sides):
            p1 = (0, 0)
            p2 = (radius * cos((1 + i * 2) * pi / sides), radius * sin((1 + i * 2) * pi / sides))
            diagonals.append(Path([p1, p2], 'u'))

        # create points for zig zag pattern
        points = []
        styles = []
        for i in range(rings):
            dy = radius * ((i + 1.) / (rings + 1.)) * sin_
            x = H * (i + 1.) / (rings + 1.)
            points.append((x, +dy))
            if i != rings:
                points.append((x, -dy))
            styles.append('v' if i % 2 == 0 else 'm')
            styles.append('u')
        points.append((H, radius * sin_))

        # create zig-zag pattern and correct it according to desired pattern
        zig_zag = Path.generate_separated_paths(points, styles)
        if pattern == "classic":
            zig_zag = [p for p in zig_zag if p.style != 'u']
        elif pattern == "alternate_asymmetric":
            for i in range(len(zig_zag)):
                if (i + 3) % 4 == 0:
                    p1 = zig_zag[i - 1].points[0]
                    try:
                        p2 = zig_zag[i + 1].points[1]
                    except IndexError:
                        p2 = diagonals[-1].points[1]

                    zig_zag[i] = Path([p1, p2], style='u')

        # reflect zig zag pattern to create all sides
        zig_zags = [zig_zag]
        for i in range(sides-1):
            zig_zags.append(Path.list_reflect(zig_zags[i], *diagonals[i].points))

        # modify center if needed
        if simplify_center:
            for i in range(sides):
                if i % 2 == 0:
                    p2 = diagonals[i].points[1]
                    p1 = (1./(rings+1) * p2[0], 1./(rings+1) * p2[1])
                    diagonals[i] = Path([p1, p2], 'u')

        # use ending of diagonals to create edge
        edges = Path.generate_separated_paths(
            [p.points[-1] for p in diagonals],  # bottom left
            'e', closed=True)

        self.translate = (radius, radius)
        self.path_tree = [zig_zags, diagonals, edges]

# Main function, creates an instance of the Class and calls inkex.affect() to draw the origami on inkscape
if __name__ == '__main__':
    e = Hypar()  # remember to put the name of your Class here!
    e.affect()
