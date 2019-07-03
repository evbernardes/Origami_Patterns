#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Waterbomb create functions

'''
import helpers as hp
import math

class Waterbomb(hp.Pattern):
    def generate_pattern(self):
    
        # create grid
        x_grid = [self.length*i/2. for i in range(0,2*self.columns + 1)]  # each element is [i,x(i)]
        y_grid = [self.length*i/2. for i in range(0,2*self.lines + 1)]    # each element is [i,y(i)]

        # create points
        points = []
        for y in zip(y_grid):
            points.append([(x,y) for x in zip(x_grid)])
        
        # create a list for the horizontal creases and another for the vertical creases
        # alternate strokes to minimize laser cutter path
        mountain_path_h = []
        for j in range(2,2*self.lines,2):	
            # mountain_path_h.append(hp.points_to_path([ (x_grid[-1],y_grid[ j]),
            #                                         (x_grid[ 0],y_grid[ j])],inverse = j % 4 == 0))	
            mountain_path_h.append(hp.Path([(x_grid[-1],y_grid[ j]),
                                            (x_grid[ 0],y_grid[ j])],
                                            style = 'm', inverse = j % 4 == 0))
        mountain_path_v = []
        for i in range(1,2*self.columns):
            # mountain_path_v.append(hp.points_to_path([ (x_grid[ i],y_grid[-1]),
            #                                         (x_grid[ i],y_grid[ 0])],inverse = i % 2 == 0))
            mountain_path_h.append(hp.Path([(x_grid[ i],y_grid[-1]),
                                            (x_grid[ i],y_grid[ 0])],
                                            style = 'm', inverse = i % 2 == 0))
        mountains = [mountain_path_h,mountain_path_v]
        
        # create a list for valley creases
        valleys = []
        for j in range(1,2*self.lines,2):

            line_parity = ((j + 1 - int(self.phase_shift))/2)%2

            # for each line, create one valley pattern with the "pointy" side
            # up and one with the "pointy" side down. Distribute one after the
            # other according to phase

            pointy_down = [(x_grid[0],y_grid[j-line_parity])]
            for i in range(1,2*self.columns+1):
                if i % 2 == 1:
                    pointy_down.append((x_grid[i],y_grid[j + 1 - line_parity]))
                else:
                    pointy_down.append((x_grid[i],y_grid[j     - line_parity]))

            pointy_up = [(x_grid[-1],y_grid[j+line_parity])]
            for i in range(2*self.columns,-1,-1):
                if i % 2 == 1:
                    pointy_up.append((x_grid[i],y_grid[j-1+line_parity]))
                else:
                    pointy_up.append((x_grid[i],y_grid[j+line_parity]))

            # if Magic Ball, mirror upper half of first line and bottom half of last line
            if self.waterbomb_type == 'magic_ball':
                if line_parity == 1 and j == 1:                 # if first line starts with pointy side down...
                    pointy_down = [(x_grid[-1],y_grid[j-1+line_parity])]
                    for i in range(2*self.columns,-1,-1):
                        if i % 2 == 1:
                            pointy_down.append((x_grid[i],y_grid[j-2+line_parity]))
                        else:
                            pointy_down.append((x_grid[i],y_grid[j-1+line_parity]))
                elif line_parity == 0 and j == 1:               # if first line starts with pointy side up...
                    pointy_up = [(x_grid[0],y_grid[j-1-line_parity])]
                    for i in range(1,2*self.columns+1):
                        if i % 2 == 1:
                            pointy_up.append((x_grid[i],y_grid[j+0-line_parity]))
                        else:
                            pointy_up.append((x_grid[i],y_grid[j-1-line_parity]))
                elif line_parity == 1 and j == 2*self.lines-1:       # if last line starts with pointy side up...
                    pointy_up = [(x_grid[0],y_grid[j+1-line_parity])]
                    for i in range(1,2*self.columns+1):
                        if i % 2 == 1:
                            pointy_up.append((x_grid[i],y_grid[j+2-line_parity]))
                        else:
                            pointy_up.append((x_grid[i],y_grid[j+1-line_parity]))
                elif line_parity == 0 and j == 2*self.lines-1:       # if last line starts with pointy side down...
                    pointy_down = [(x_grid[-1],y_grid[j+1+line_parity])]
                    for i in range(2*self.columns,-1,-1):
                        if i % 2 == 1:
                            pointy_down.append((x_grid[i],y_grid[j  +line_parity]))
                        else:
                            pointy_down.append((x_grid[i],y_grid[j+1+line_parity]))

            # valleys.append([hp.points_to_path(pointy_up),hp.points_to_path(pointy_down)])
            valleys.append([hp.Path(pointy_up,style = 'v'),
                            hp.Path(pointy_down,style = 'v')])

        # create a list for enclosure strokes
        enclosures = hp.Path.generate_separated_paths(
            [   (x_grid[ 0],y_grid[ 0]), # top left
                (x_grid[-1],y_grid[ 0]), # top right
                (x_grid[-1],y_grid[-1]), # bottom right
                (x_grid[ 0],y_grid[-1])],# bottom left
            'e',closed=True)
        
        self.path_tree = [mountains,valleys,enclosures]
    
    # def __init__(self,lines,columns,length,styles_dict,group,phase_shift = False, magic_ball = False):
    def __init__(self,lines,columns,length,phase_shift = False, waterbomb_type = 'regular'):
        self.lines = lines
        self.columns = columns
        self.length = length
        self.phase_shift = phase_shift
        self.waterbomb_type = waterbomb_type
        self.generate_pattern()
