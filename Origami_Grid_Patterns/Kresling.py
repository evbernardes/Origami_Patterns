#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Helper functions

'''
from helpers import *
import math

def create_kresling(lines,n,R,angle_ratio):
    theta = (math.pi/2.)*(1 - 2./n)
    l = 2.*R*math.cos(theta*(1.-angle_ratio))
    a = 2.*R*math.sin(math.pi/n)
    b = math.sqrt(a*a + l*l - 2*a*l*math.cos(angle_ratio*theta))

    phi = abs(math.acos((l*l + b*b - a*a)/(2*l*b)))
    gamma = math.pi/2 - angle_ratio*theta - phi
    dy = b*math.cos(gamma)
    dx = b*math.sin(gamma)
    
    # create grid
    x_grid = []
    y_grid = []
    for j in range(lines,-1,-1):
        x_grid_ = [dx*j + a*i for i in range(0,n + 1)]
        x_grid.append(x_grid_)
    y_grid = [dy*j for j in range(0,lines + 1)]
    

    # create points
    points = []
    # for y in zip(*y_grid)[1]:
    #     points.append([(x,y) for x in zip(*x_grid)[1]])
    
    # create a list for the horizontal creases and another for the vertical creases
    mountain_path_h = []
    for i in range(1,lines):
        mountain_path_h.append(points_to_path([ (x_grid[i][ 0],y_grid[ i]),
                                                (x_grid[i][-1],y_grid[ i])],inverse = i % 2 == 0))

    mountain_path_v = []
    for i in range(1,n):
        mountain_path_h.append(points_to_path([ (x_grid[ 0][i],y_grid[ 0]),
                                                (x_grid[-1][i],y_grid[-1])],inverse = i % 2 == 0))
    mountains = [mountain_path_h,mountain_path_v]
    
    # create a list for valley creases
    valleys = []
    for i in range(1,n+lines):
        diff_x = max(i - (len(x_grid[0])-1),0)  # account for limits of grid
        diff_y = max(i - (len(x_grid)-1),0)     # in both directions
        valleys.append(points_to_path([ (x_grid[i-diff_y][  diff_y],y_grid[i-diff_y]),
                                        (x_grid[  diff_x][i-diff_x],y_grid[  diff_x])],inverse = i % 2 == 0))


    # create a list for enclosure strokes
    enclosures = points_to_enclosure([(x_grid[ 0][ 0],y_grid[ 0]), # top left
                                      (x_grid[ 0][-1],y_grid[ 0]), # top right
                                      (x_grid[-1][-1],y_grid[-1]), # bottom right
                                      (x_grid[-1][ 0],y_grid[-1])])# bottom left                                 
    return points,mountains,valleys,enclosures

def create_kresling_radial(lines,n,R,radial_ratio,min_polygon = False):
    if min_polygon == True:
        n = int(math.ceil(2. / (1. - (4./math.pi)*math.asin(radial_ratio))))
    max_radial_ratio = math.sin((math.pi/4)*(1. - 2./n))
    if (radial_ratio > max_radial_ratio):
        # inkex.debug('Radial ratio of value {} chosen, but the max value of {} was used instead.'.format(radial_ratio,max_radial_ratio))
        radial_ratio = max_radial_ratio
    angular_ratio = 1 - 2*n*math.asin(radial_ratio)/((n-2)*math.pi)
    return create_kresling(lines,n,R,angular_ratio)
    # return points,mountains,valleys,enclosures
