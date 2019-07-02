#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Helper functions

'''
import inkex       # Required
import simplestyle # will be needed here for styles support

'''
Pattern Mother Class

Only here so patterns can be inherited classes of it

'''
class Pattern:
    def draw_path_tree(self,group,styles_dict):
        create_path_recursively(self.path_tree,group,styles_dict)


def create_path_recursively(path_tree,group,styles_dict):
        for subpath in path_tree:
            if type(subpath) == list:
                subgroup = inkex.etree.SubElement(group, 'g')
                create_path_recursively(subpath,subgroup,styles_dict)
            else:
                # inkex.debug("{},{}".format(subpath.style,subpath.path))
                attribs = { 'style': simplestyle.formatStyle(styles_dict[subpath.style]), 'd': subpath.path}
                inkex.etree.SubElement(group, inkex.addNS('path','svg'), attribs )

'''
Path Class

Defines a path and what it is supposed to be (mountain, valley, enclosure)

'''
class Path:
    def generate_path(self):
        self.path = ''
        if(self.inverse):
            points = self.points[::-1]
        else:
            points = self.points
        for i in range(len(points)-1):
            self.path = self.path+'M{},{}L{},{}'.format(points[i][0],points[i][1],points[i+1][0],points[i+1][1])
        if self.closed:
            self.path = self.path+'M{},{}L{},{}z'.format(points[-1][0],points[-1][1],points[0][0],points[0][1])
        return self.path

    def __init__(self,points,style,closed=False,inverse=False):
        self.points = points
        self.style = style
        self.closed = closed
        self.inverse = inverse
        self.generate_path()

def generate_separated_paths(points,style,closed=False):
    paths = []
    for i in range(len(points) - 1 + int(closed)):
        j = (i+1)%len(points)
        paths.append(Path([(points[ i][ 0],points[ i][1]),
                           (points[ j][ 0],points[ j][1])],style))
    return paths


