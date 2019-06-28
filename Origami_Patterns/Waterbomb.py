#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Waterbomb create functions

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

        line_parity = ((j + 1 - int(phase_shift))/2)%2

        # for each line, create one valley pattern with the "pointy" side
        # up and one with the "pointy" side down. Distribute one after the
        # other according to phase

        pointy_down = [(x_grid[0],y_grid[j-line_parity])]
        for i in range(1,2*columns+1):
            if i % 2 == 1:
                pointy_down.append((x_grid[i],y_grid[j + 1 - line_parity]))
            else:
                pointy_down.append((x_grid[i],y_grid[j     - line_parity]))

        pointy_up = [(x_grid[-1],y_grid[j+line_parity])]
        for i in range(2*columns,-1,-1):
            if i % 2 == 1:
                pointy_up.append((x_grid[i],y_grid[j-1+line_parity]))
            else:
                pointy_up.append((x_grid[i],y_grid[j+line_parity]))

        # if Magic Ball, mirror upper half of first line and bottom half of last line
        if magic_ball:
            if line_parity == 1 and j == 1:                 # if first line starts with pointy side down...
                pointy_down = [(x_grid[-1],y_grid[j-1+line_parity])]
                for i in range(2*columns,-1,-1):
                    if i % 2 == 1:
                        pointy_down.append((x_grid[i],y_grid[j-2+line_parity]))
                    else:
                        pointy_down.append((x_grid[i],y_grid[j-1+line_parity]))
            elif line_parity == 0 and j == 1:               # if first line starts with pointy side up...
                pointy_up = [(x_grid[0],y_grid[j-1-line_parity])]
                for i in range(1,2*columns+1):
                    if i % 2 == 1:
                        pointy_up.append((x_grid[i],y_grid[j+0-line_parity]))
                    else:
                        pointy_up.append((x_grid[i],y_grid[j-1-line_parity]))
            elif line_parity == 1 and j == 2*lines-1:       # if last line starts with pointy side up...
                pointy_up = [(x_grid[0],y_grid[j+1-line_parity])]
                for i in range(1,2*columns+1):
                    if i % 2 == 1:
                        pointy_up.append((x_grid[i],y_grid[j+2-line_parity]))
                    else:
                        pointy_up.append((x_grid[i],y_grid[j+1-line_parity]))
            elif line_parity == 0 and j == 2*lines-1:       # if last line starts with pointy side down...
                pointy_down = [(x_grid[-1],y_grid[j+1+line_parity])]
                for i in range(2*columns,-1,-1):
                    if i % 2 == 1:
                        pointy_down.append((x_grid[i],y_grid[j  +line_parity]))
                    else:
                        pointy_down.append((x_grid[i],y_grid[j+1+line_parity]))

        valleys.append([points_to_path(pointy_up),points_to_path(pointy_down)])

    # create a list for enclosure strokes
    enclosures = points_to_enclosure([(x_grid[ 0],y_grid[ 0]), # top left
                                      (x_grid[-1],y_grid[ 0]), # top right
                                      (x_grid[-1],y_grid[-1]), # bottom right
                                      (x_grid[ 0],y_grid[-1])])# bottom left
	
    return points,mountains,valleys,enclosures


