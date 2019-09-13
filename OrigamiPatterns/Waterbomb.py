#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

import inkex

from Path import Path
from Pattern import Pattern

# TODO:
# Add fractional column number option


class Waterbomb(Pattern):
    
    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="waterbomb",
                                     help="Origami pattern")

        self.OptionParser.add_option("", "--pattern_first_line",
                                     action="store", type="string",
                                     dest="pattern_first_line", default="waterbomb",
                                     help="Origami pattern")

        self.OptionParser.add_option("", "--pattern_last_line",
                                     action="store", type="string",
                                     dest="pattern_last_line", default="waterbomb",
                                     help="Origami pattern")
        
        self.OptionParser.add_option("", "--lines",
                                     action="store", type="int",
                                     dest="lines", default=8,
                                     help="Number of lines")
        
        self.OptionParser.add_option("", "--columns",
                                     action="store", type="int", 
                                     dest="columns", default=16,
                                     help="Number of columns")

        self.OptionParser.add_option("", "--length",
                                     action="store", type="float", 
                                     dest="length", default=10.0,
                                     help="Length of grid square")
        
        self.OptionParser.add_option('', '--phase_shift', action='store',
                                     type='inkbool', dest='phase_shift',
                                     default=True,
                                     help='Shift phase of tesselation.')
    
    def generate_path_tree(self):
        """ Specialized path generation for Waterbomb tesselation pattern
        """
        unit_factor = self.calc_unit_factor()
        length = self.options.length * unit_factor
        vertex_radius = self.options.vertex_radius * unit_factor
        cols = self.options.columns
        lines = self.options.lines
        phase_shift = self.options.phase_shift
        pattern_first_line = self.options.pattern_first_line
        pattern_last_line = self.options.pattern_last_line

        # create vertices
        vertex_line_types = [[Path(((i / 2.) * length, 0), style='p', radius=vertex_radius) for i in range(2*cols + 1)],
                             [Path((i * length, 0), style='p', radius=vertex_radius) for i in range(cols + 1)],
                             [Path(((i + 0.5) * length, 0), style='p', radius=vertex_radius) for i in range(cols)]]

        vertices = []
        for i in range(2*lines + 1):
            if i % 2 == 0 or (pattern_first_line == 'magic_ball' and i == 1) or (pattern_last_line == 'magic_ball' and i == 2*lines - 1):
                type = 0
            elif(i/2 + phase_shift) % 2 == 0:
                type = 1
            else:
                type = 2
            vertices = vertices + Path.list_add(vertex_line_types[type], (0, 0.5*i*length))

        # create a list for the horizontal creases and another for the vertical creases
        # alternate strokes to minimize laser cutter path
        corr_fist_line = length/2 if pattern_first_line == 'magic_ball' else 0
        corr_last_line = length/2 if pattern_last_line == 'magic_ball' else 0
        grid = [Path.generate_hgrid([0, length*cols],    [0,      length*lines],  lines, 'm'),
                Path.generate_vgrid([0, length*cols], [corr_fist_line, length*lines-corr_last_line], 2*cols, 'm')]

        vgrid_a = Path.generate_vgrid([0, length * cols], [0, length / 2], 2 * cols, 'v')
        vgrid_b = Path.list_add(vgrid_a, (0, (lines - 0.5) * length))
        if pattern_first_line == 'magic_ball' and pattern_last_line == 'magic_ball':
            grid[1] = [[vgrid_a[i], grid[1][i], vgrid_b[i]] if i % 2 == 0 else
                       [vgrid_b[i], grid[1][i], vgrid_a[i]] for i in range(len(grid[1]))]
        elif pattern_first_line == 'magic_ball':
            grid[1] = [[vgrid_a[i], grid[1][i]] if i % 2 == 0 else
                       [grid[1][i], vgrid_a[i]] for i in range(len(grid[1]))]
        elif pattern_last_line == 'magic_ball':
            grid[1] = [[grid[1][i], vgrid_b[i]] if i % 2 == 0 else
                       [vgrid_b[i], grid[1][i]] for i in range(len(grid[1]))]

        # create generic valley Path lines, one pointing up and other pointing down
        valley_types = [Path([(i * length / 2, (1 - i % 2) * length / 2) for i in range(2 * cols + 1)], 'v'),
                        Path([(    i*length/2,         (i % 2)*length/2) for i in range(2 * cols + 1)], 'v')]

        # define which lines must be of which type, according to parity and options
        senses = np.array([bool((i % 2+i)/2 % 2) for i in range(2*lines)])
        if phase_shift:
            senses = np.invert(senses)
        if pattern_first_line == "magic_ball":
            senses[0] = ~senses[0]
        if pattern_last_line == "magic_ball":
            senses[-1] = ~senses[-1]
        valleys = [valley_types[senses[i]] + (0, i * length / 2) for i in range(2*lines)]

        # convert first and last lines to mountains if magic_ball
        if pattern_first_line == "magic_ball":
            valleys[0].style = 'm'
        if pattern_last_line == "magic_ball":
            valleys[-1].style = 'm'

        # invert every two lines to minimize laser cutter movements
        for i in range(1, 2*lines, 2):
            valleys[i].invert()

        self.edge_points = [(0*length*cols, 0*length*lines),   # top left
                       (1*length*cols, 0*length*lines),   # top right
                       (1*length*cols, 1*length*lines),   # bottom right
                       (0*length*cols, 1*length*lines)]  # bottom left
        
        self.path_tree = [grid, valleys, vertices]


if __name__ == '__main__':

    e = Waterbomb()
    e.affect()
