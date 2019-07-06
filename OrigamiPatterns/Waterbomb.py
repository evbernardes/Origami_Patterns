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
        mountains = [Path.generate_hgrid([0, length*cols], [0, length*lines],  lines, 'm'),
                     Path.generate_vgrid([0, length*cols], [0, length*lines], 2*cols, 'm')]

        # create generic valley Path lines
        points = []
        for i in range(2 * cols + 1):
            points.append((i * length / 2, (1 - i % 2) * length / 2))
        Path_type_1 = Path(points, 'v')     # lines with "pointy parts" up

        points = []
        for i in range(2*cols + 1):
            points.append((i*length/2, (i % 2)*length/2))
        Path_type_2 = Path(points, 'v')    # lines with "pointy parts" down

        # define which lines must be of which type, according to parity and options
        senses = np.array([bool((i % 2+i)/2 % 2) for i in range(2*lines)])
        if phase_shift:
            senses = np.invert(senses)
        if pattern == "magic_ball":
            senses[0] = ~senses[0]
            senses[-1] = ~senses[-1]

        valleys = []
        for i in range(2*lines):
            if senses[i]:
                valleys.append(Path_type_1 + (0, i * length / 2))
            else:
                valleys.append(Path_type_2 + (0, i * length / 2))

        # create a list for edge strokes
        edges = Path.generate_separated_paths(
            [(0*length*cols, 0*length*lines),   # top left
             (1*length*cols, 0*length*lines),   # top right
             (1*length*cols, 1*length*lines),   # bottom right
             (0*length*cols, 1*length*lines)],  # bottom left
            'e', closed=True)
        
        self.path_tree = [mountains, valleys, edges]


if __name__ == '__main__':

    e = Waterbomb()
    e.affect()
