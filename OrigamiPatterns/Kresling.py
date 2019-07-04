#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import inkex

from Path import Path
from Pattern import Pattern


class Kresling(Pattern):

    def __init__(self):
        ''' Constructor
        '''
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

    def generate_path_tree(self):
        ''' Specialized path generation for Waterbomb tesselation pattern
        '''
        theta = (math.pi/2.)*(1 - 2./self.options.sides)
        l = 2.*self.options.radius*math.cos(theta*(1.-self.options.angle_ratio))
        a = 2.*self.options.radius*math.sin(math.pi/self.options.sides)
        b = math.sqrt(a*a + l*l - 2*a*l*math.cos(self.options.angle_ratio*theta))

        phi = abs(math.acos((l*l + b*b - a*a)/(2*l*b)))
        gamma = math.pi/2 - self.options.angle_ratio*theta - phi
        dy = b*math.cos(gamma)
        dx = b*math.sin(gamma)
        
        # create grid
        x_grid = []
        y_grid = []
        for j in range(self.options.lines,-1,-1):
            x_grid_ = [dx*j + a*i for i in range(0,self.options.sides + 1)]
            x_grid.append(x_grid_)
        y_grid = [dy*j for j in range(0,self.options.lines + 1)]

        # create points
        # points = []
        # for y in zip(*y_grid)[1]:
        #     points.append([(x,y) for x in zip(*x_grid)[1]])
        
        # create a list for the horizontal creases and another for the vertical creases
        mountain_path_h = []
        for i in range(1,self.options.lines):
            mountain_path_h.append(Path([(x_grid[i][ 0],y_grid[ i]),
                                         (x_grid[i][-1],y_grid[ i])],
                                        'm',inverse = i % 2 == 0))

        mountain_path_v = []
        for i in range(1,self.options.sides):
            mountain_path_h.append(Path([(x_grid[ 0][i],y_grid[ 0]),
                                         (x_grid[-1][i],y_grid[-1])],
                                        'm',inverse = i % 2 == 0))
        mountains = [mountain_path_h,mountain_path_v]
        
        # create a list for valley creases
        valleys = []
        for i in range(1,self.options.sides+self.options.lines):
            diff_x = max(i - (len(x_grid[0])-1),0)  # account for limits of grid
            diff_y = max(i - (len(x_grid)-1),0)     # in both directions
            valleys.append(Path([(x_grid[i-diff_y][  diff_y],y_grid[i-diff_y]),
                                 (x_grid[  diff_x][i-diff_x],y_grid[  diff_x])],
                                'v',inverse = i % 2 == 0))

        # create a list for enclosure strokes        
        enclosures = Path.generate_separated_paths(
            [(x_grid[ 0][ 0],y_grid[ 0]), # top left
             (x_grid[ 0][-1],y_grid[ 0]), # top right
             (x_grid[-1][-1],y_grid[-1]), # bottom right
             (x_grid[-1][ 0],y_grid[-1])],# bottom left
            'e',closed=True) 
        
        self.path_tree = [mountains,valleys,enclosures]

if __name__ == '__main__':
    e = Kresling()
    e.affect()