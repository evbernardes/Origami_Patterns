#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Helper functions

'''
from helpers import *
import math

def create_waterbomb(lines,columns,length,phase_shift = False, magic_ball = False):
    
    # create grid
    x_grid = [length*i/2. for i in range(0,2*columns + 1)]  # each element is [i,x(i)]
    y_grid = [length*i/2. for i in range(0,2*lines + 1)]    # each element is [i,y(i)]

    # create points
    points = []
    for y in zip(y_grid):
        points.append([(x,y) for x in zip(x_grid)])
    
    # create a list for the horizontal creases and another for the vertical creases
    # alternate strokes to minimize laser cutter path
    mountain_path_h = []
    for j in range(2,2*lines,2):	
        mountain_path_h.append(points_to_path([ (x_grid[-1],y_grid[ j]),
                                                (x_grid[ 0],y_grid[ j])],inverse = j % 4 == 0))
    mountain_path_v = []
    for i in range(1,2*columns):
        mountain_path_v.append(points_to_path([ (x_grid[ i],y_grid[-1]),
                                                (x_grid[ i],y_grid[ 0])],inverse = i % 2 == 0))
    mountains = [mountain_path_h,mountain_path_v]
    
    # create a list for valley creases
    valleys = []
    for j in range(1,2*lines,2):

        if ((j + int(phase_shift))/2)%2 == 0: # odd lines

            top_points = [(x_grid[0],y_grid[j-1])]
            for i in range(1,2*columns+1):  # upper half
                if i % 2 == 1:
                    top_points.append((x_grid[i],y_grid[  j]))
                else:
                    top_points.append((x_grid[i],y_grid[j-1]))


            bottom_points = [(x_grid[-1],y_grid[j+1])]
            for i in range(2*columns,0,-1): # bottom half
                if i % 2 == 1:
                    bottom_points.append((x_grid[i],y_grid[  j]))
                else:
                    bottom_points.append((x_grid[i],y_grid[j+1]))
            bottom_points.append((x_grid[0],y_grid[j+1]))

        else:                                   # even lines
            top_points = [(x_grid[0],y_grid[j])]
            for i in range(1,2*columns+1):  # upper half
                if i % 2 == 0:
                    top_points.append((x_grid[i],y_grid[  j]))
                else:
                    top_points.append((x_grid[i],y_grid[j-1]))

            bottom_points = []    
            for i in range(2*columns,0,-1): # bottom half
                if i % 2 == 0:
                    bottom_points.append((x_grid[i],y_grid[  j]))
                else:
                    bottom_points.append((x_grid[i],y_grid[j+1]))
            bottom_points.append((x_grid[0],y_grid[j]))

        valleys.append([points_to_path(top_points),points_to_path(bottom_points)])

    # create a list for enclosure strokes
    enclosures = points_to_enclosure([(x_grid[ 0],y_grid[ 0]), # top left
                                      (x_grid[-1],y_grid[ 0]), # top right
                                      (x_grid[-1],y_grid[-1]), # bottom right
                                      (x_grid[ 0],y_grid[-1])])# bottom left
	
    return points,mountains,valleys,enclosures

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

