#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

from Path import Path
from Pattern import Pattern


class Waterbomb(Pattern):
    
    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="waterbomb",
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
        length = self.options.length
        cols = self.options.columns
        lines = self.options.lines
        phase_shift = self.options.phase_shift
        pattern = self.options.pattern
        
        # # create grid
        # x_grid = [length*i/2. for i in range(0, 2*cols + 1)]  # each element is [i,x(i)]
        # y_grid = [length*i/2. for i in range(0, 2*lines + 1)]    # each element is [i,y(i)]
        #
        # # create points
        # points = []
        # for y in zip(y_grid):
        #     points.append([(x, y) for x in zip(x_grid)])
        
        # create a list for the horizontal creases and another for the vertical creases
        # alternate strokes to minimize laser cutter path
        corr = length/2 if pattern == 'magic_ball' else 0
        grid = [Path.generate_hgrid([0, length*cols],    [0,      length*lines],  lines, 'm'),
                Path.generate_vgrid([0, length*cols], [corr, length*lines-corr], 2*cols, 'm')]
        if pattern == 'magic_ball':
            vgrid_a = Path.generate_vgrid([0, length*cols], [0, length/2], 2*cols, 'v')
            vgrid_b = Path.list_add(vgrid_a, (0, (lines-0.5)*length))
            grid[1] = [[vgrid_a[i], grid[1][i], vgrid_b[i]] if i % 2 == 0 else
                       [vgrid_b[i], grid[1][i], vgrid_a[i]] for i in range(len(grid[1]))]

        # create generic valley Path lines, one pointing up and other pointing down
        valley_types = [Path([(i * length / 2, (1 - i % 2) * length / 2) for i in range(2 * cols + 1)], 'v'),
                        Path([(    i*length/2,         (i % 2)*length/2) for i in range(2 * cols + 1)], 'v')]

        # define which lines must be of which type, according to parity and options
        senses = np.array([bool((i % 2+i)/2 % 2) for i in range(2*lines)])
        if phase_shift:
            senses = np.invert(senses)
        if pattern == "magic_ball":
            senses[0] = ~senses[0]
            senses[-1] = ~senses[-1]
        valleys = [valley_types[senses[i]] + (0, i * length / 2) for i in range(2*lines)]

        # convert first and last lines to mountains if magic_ball
        if pattern == "magic_ball":
            valleys[0].style = 'm'
            valleys[-1].style = 'm'

        # invert every two lines to minimize laser cutter movements
        for i in range(1, 2*lines, 2):
            valleys[i].invert()

        edges = Path.generate_separated_paths(
            [(0*length*cols, 0*length*lines),   # top left
             (1*length*cols, 0*length*lines),   # top right
             (1*length*cols, 1*length*lines),   # bottom right
             (0*length*cols, 1*length*lines)],  # bottom left
            'e', closed=True)
        
        self.path_tree = [grid, valleys, edges]


if __name__ == '__main__':

    e = Waterbomb()
    e.affect()
