#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Helper functions

'''
import helpers as hp
import math
import inkex

class Kresling(hp.Pattern):
    def generate_pattern(self):

        theta = (math.pi/2.)*(1 - 2./self.sides)
        l = 2.*self.radius*math.cos(theta*(1.-self.angle_ratio))
        a = 2.*self.radius*math.sin(math.pi/self.sides)
        b = math.sqrt(a*a + l*l - 2*a*l*math.cos(self.angle_ratio*theta))

        phi = abs(math.acos((l*l + b*b - a*a)/(2*l*b)))
        gamma = math.pi/2 - self.angle_ratio*theta - phi
        dy = b*math.cos(gamma)
        dx = b*math.sin(gamma)
        
        # create grid
        x_grid = []
        y_grid = []
        for j in range(self.lines,-1,-1):
            x_grid_ = [dx*j + a*i for i in range(0,self.sides + 1)]
            x_grid.append(x_grid_)
        y_grid = [dy*j for j in range(0,self.lines + 1)]
        

        # create points
        points = []
        # for y in zip(*y_grid)[1]:
        #     points.append([(x,y) for x in zip(*x_grid)[1]])
        
        # create a list for the horizontal creases and another for the vertical creases
        mountain_path_h = []
        for i in range(1,self.lines):
            mountain_path_h.append(hp.Path([(x_grid[i][ 0],y_grid[ i]),
                                            (x_grid[i][-1],y_grid[ i])],
                                            'm',inverse = i % 2 == 0))

        mountain_path_v = []
        for i in range(1,self.sides):
            mountain_path_h.append(hp.Path([(x_grid[ 0][i],y_grid[ 0]),
                                            (x_grid[-1][i],y_grid[-1])],
                                            'm',inverse = i % 2 == 0))
        mountains = [mountain_path_h,mountain_path_v]
        
        # create a list for valley creases
        valleys = []
        for i in range(1,self.sides+self.lines):
            diff_x = max(i - (len(x_grid[0])-1),0)  # account for limits of grid
            diff_y = max(i - (len(x_grid)-1),0)     # in both directions
            valleys.append(hp.Path([(x_grid[i-diff_y][  diff_y],y_grid[i-diff_y]),
                                    (x_grid[  diff_x][i-diff_x],y_grid[  diff_x])],
                                    'v',inverse = i % 2 == 0))

        # create a list for enclosure strokes        
        enclosures = hp.Path.generate_separated_paths(
            [   (x_grid[ 0][ 0],y_grid[ 0]), # top left
                (x_grid[ 0][-1],y_grid[ 0]), # top right
                (x_grid[-1][-1],y_grid[-1]), # bottom right
                (x_grid[-1][ 0],y_grid[-1])],# bottom left
            'e',closed=True) 
        
        self.path_tree = [mountains,valleys,enclosures]
    
    def __init__(self,lines,sides,radius,angle_ratio):
        self.lines = lines
        self.sides = sides
        self.radius = radius
        self.angle_ratio = angle_ratio
        # self.kresling_type = kresling_type
        self.generate_pattern()

class Kresling_radial(Kresling):
    def __init__(self,lines,sides,radius,radial_ratio,min_polygon = False):
        self.lines = lines
        self.radius = radius

        if min_polygon == True:
            self.sides = max(3,int(math.ceil(2. / (1. - (4./math.pi)*math.asin(radial_ratio)))))
        else:
            self.sides = sides

        max_radial_ratio = math.sin((math.pi/4)*(1. - 2./self.sides))
        if (radial_ratio > max_radial_ratio):
            inkex.errormsg(_("For polygon of {} sides, the maximal radial ratio is = {}\nLower ratio, increase number of sides or select \"Minimize polygon sides\" option.".format(self.sides,max_radial_ratio)))
            # inkex.debug('Radial ratio of value {} chosen, but the max value of {} was used instead.'.format(radial_ratio,max_radial_ratio))
            radial_ratio = max_radial_ratio
        self.angle_ratio = 1 - 2*self.sides*math.asin(radial_ratio)/((self.sides-2)*math.pi)

        self.generate_pattern()
        