#! /usr/bin/env python
# -*- coding: utf-8 -*-
from math import pi, sin, cos, acos, sqrt
import inkex

from Path import Path
from Pattern import Pattern


class Kresling(Pattern):

    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="kresling",
                                     help="Origami pattern")      
        
        self.OptionParser.add_option("", "--lines",
                                     action="store", type="int",
                                     dest="lines", default=1,
                                     help="Number of lines")
        
        self.OptionParser.add_option("", "--sides",
                                     action="store", type="int", 
                                     dest="sides", default=3,
                                     help="Number of polygon sides")

        self.OptionParser.add_option("", "--angle_ratio",
                                     action="store", type="float", 
                                     dest="angle_ratio", default=0.5,
                                     help="Angle ratio")

        self.OptionParser.add_option("", "--radius",
                                     action="store", type="float", 
                                     dest="radius", default=10.0,
                                     help="Radius of tower (mm)")

    @staticmethod
    def generate_kresling_zigzag(sides, radius, angle_ratio):

        theta = (pi / 2.) * (1 - 2. / sides)
        length = 2. * radius * cos(theta * (1. - angle_ratio))
        a = 2. * radius * sin(pi / sides)
        b = sqrt(a * a + length * length - 2 * a * length * cos(angle_ratio * theta))

        phi = abs(acos((length * length + b * b - a * a) / (2 * length * b)))
        gamma = pi / 2 - angle_ratio * theta - phi
        dy = b * cos(gamma)
        dx = b * sin(gamma)

        points = []
        styles = []

        for i in range(sides):
            points.append((i * a, 0))
            points.append(((i + 1) * a + dx, -dy))
            styles.append('v')
            if i != sides - 1:
                styles.append('m')

        path = Path.generate_separated_paths(points, styles)
        return path

    def generate_path_tree(self):
        """ Specialized path generation for Waterbomb tesselation pattern
        """
        unit_factor = self.calc_unit_factor()
        lines = self.options.lines
        sides = self.options.sides
        radius = self.options.radius * unit_factor
        angle_ratio = self.options.angle_ratio

        theta = (pi/2.)*(1 - 2./sides)
        length = 2.*radius*cos(theta*(1.-angle_ratio))
        a = 2.*radius*sin(pi/sides)
        b = sqrt(a*a + length*length - 2*a*length*cos(angle_ratio*theta))

        phi = abs(acos((length*length + b*b - a*a)/(2*length*b)))
        gamma = pi/2 - angle_ratio*theta - phi
        dy = b*cos(gamma)
        dx = b*sin(gamma)
        
        # # create grid
        # x_grid = []
        # for j in range(lines, -1, -1):
        #     x_grid_ = [dx*j + a*i for i in range(0, sides + 1)]
        #     x_grid.append(x_grid_)
        # y_grid = [dy*j for j in range(0, lines + 1)]

        # create points
        # points = []
        # for y in zip(*y_grid)[1]:
        #     points.append([(x,y) for x in zip(*x_grid)[1]])
        
        # create a horizontal grid, then offset each line according to angle
        grid_h = Path.generate_hgrid([0, a * sides], [0, dy * lines], lines, 'm')
        grid_h = Path.list_add(grid_h, [(i*dx, 0) for i in range(lines-1, 0, -1)])

        zigzag = Kresling.generate_kresling_zigzag(sides, radius, angle_ratio)
        zigzags = []
        for i in range(lines):
            zigzags.append(Path.list_add(zigzag, (i * dx, (lines - i) * dy)))

        # create a list for edge strokes        
        edges = Path.generate_separated_paths(
            [(dx*lines          , 0         ),   # top left
             (dx*lines + a*sides, 0         ),   # top right
             (a*sides           , dy*lines  ),   # bottom right
             (0                 , dy*lines  )],  # bottom left
            'e', closed=True)

        self.path_tree = [grid_h, zigzags, edges]


if __name__ == '__main__':

    e = Kresling()
    e.affect()
