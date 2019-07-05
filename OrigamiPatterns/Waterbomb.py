#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math

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
        # TODO: refactor code using:
        # a = np.array([bool((i%2+i)/2 %2) for i in range(2*lines)])
        # if phase_shift:
        #     a.invert()
        # if magic_ball:
        #     a[0] = ~a[0]
        #     a[-1] = ~a[-1]

        # create grid
        x_grid = [self.options.length*i/2. for i in range(0, 2*self.options.columns + 1)]  # each element is [i,x(i)]
        y_grid = [self.options.length*i/2. for i in range(0, 2*self.options.lines + 1)]    # each element is [i,y(i)]

        # create points
        points = []
        for y in zip(y_grid):
            points.append([(x, y) for x in zip(x_grid)])
        
        # create a list for the horizontal creases and another for the vertical creases
        # alternate strokes to minimize laser cutter path
        mountain_path_h = []
        for j in range(2, 2*self.options.lines, 2):
            mountain_path_h.append(Path([(x_grid[-1], y_grid[ j]),
                                         (x_grid[ 0], y_grid[ j])],
                                        style='m', inverse=j % 4 == 0))
        mountain_path_v = [] 
        for i in range(1, 2*self.options.columns):
            mountain_path_h.append(Path([(x_grid[ i], y_grid[-1]),
                                         (x_grid[ i], y_grid[ 0])],
                                        style='m', inverse=i % 2 == 0))
        mountains = [mountain_path_h, mountain_path_v]
        
        # create a list for valley creases
        valleys = []
        for j in range(1, 2*self.options.lines,2):

            line_parity = ((j + 1 - int(self.options.phase_shift))/2) % 2

            # for each line, create one valley pattern with the "pointy" side
            # up and one with the "pointy" side down. Distribute one after the
            # other according to phase

            pointy_down = [(x_grid[0], y_grid[j-line_parity])]
            for i in range(1, 2*self.options.columns+1):
                if i % 2 == 1:
                    pointy_down.append((x_grid[i], y_grid[j + 1 - line_parity]))
                else:
                    pointy_down.append((x_grid[i], y_grid[j     - line_parity]))

            pointy_up = [(x_grid[-1], y_grid[j+line_parity])]
            for i in range(2*self.options.columns, -1, -1):
                if i % 2 == 1:
                    pointy_up.append((x_grid[i], y_grid[j-1+line_parity]))
                else:
                    pointy_up.append((x_grid[i], y_grid[j+line_parity]))

            # if Magic Ball, mirror upper half of first line and bottom half of last line
            if self.options.pattern == 'magic_ball':
                if line_parity == 1 and j == 1:                 # if first line starts with pointy side down...
                    pointy_down = [(x_grid[-1], y_grid[j-1+line_parity])]
                    for i in range(2*self.options.columns, -1, -1):
                        if i % 2 == 1:
                            pointy_down.append((x_grid[i], y_grid[j-2+line_parity]))
                        else:
                            pointy_down.append((x_grid[i], y_grid[j-1+line_parity]))
                elif line_parity == 0 and j == 1:               # if first line starts with pointy side up...
                    pointy_up = [(x_grid[0], y_grid[j-1-line_parity])]
                    for i in range(1, 2*self.options.columns+1):
                        if i % 2 == 1:
                            pointy_up.append((x_grid[i], y_grid[j+0-line_parity]))
                        else:
                            pointy_up.append((x_grid[i], y_grid[j-1-line_parity]))
                elif line_parity == 1 and j == 2*self.options.lines-1:    # if last line starts with pointy side up...
                    pointy_up = [(x_grid[0], y_grid[j+1-line_parity])]
                    for i in range(1, 2*self.options.columns+1):
                        if i % 2 == 1:
                            pointy_up.append((x_grid[i], y_grid[j+2-line_parity]))
                        else:
                            pointy_up.append((x_grid[i], y_grid[j+1-line_parity]))
                elif line_parity == 0 and j == 2*self.options.lines-1:    # if last line starts with pointy side down...
                    pointy_down = [(x_grid[-1], y_grid[j+1+line_parity])]
                    for i in range(2*self.options.columns, -1, -1):
                        if i % 2 == 1:
                            pointy_down.append((x_grid[i], y_grid[j  +line_parity]))
                        else:
                            pointy_down.append((x_grid[i], y_grid[j+1+line_parity]))

            valleys.append([Path(pointy_up, style='v'),
                            Path(pointy_down, style='v')])

        # create a list for edge strokes
        edges = Path.generate_separated_paths(
            [   (x_grid[ 0], y_grid[ 0]),   # top left
                (x_grid[-1], y_grid[ 0]),   # top right
                (x_grid[-1], y_grid[-1]),   # bottom right
                (x_grid[ 0], y_grid[-1])],  # bottom left
            'e', closed=True)
        
        self.path_tree = [mountains, valleys, edges]


if __name__ == '__main__':

    e = Waterbomb()
    e.affect()
