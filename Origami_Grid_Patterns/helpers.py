#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Helper functions

'''
import inkex       # Required
import simplestyle # will be needed here for styles support

def points_to_path(points,closed=False,inverse=False):
    path = ''
    if(inverse):
        points = points[::-1]
    for i in range(len(points)-1):
        path = path+'M{},{}L{},{}'.format(points[i][0],points[i][1],points[i+1][0],points[i+1][1])
    if closed:
        path = path+'M{},{}L{},{}z'.format(points[-1][0],points[-1][1],points[0][0],points[0][1])
    return path

def points_to_enclosure(points):
    enclosures = []
    for i in range(len(points)):
        j = (i+1)%len(points)
        enclosures.append(points_to_path([  (points[ i][ 0],points[ i][1]),
                                            (points[ j][ 0],points[ j][1])]))
    return enclosures

def paths_to_group(paths,group,style):
    for subpaths in paths:
        if type(subpaths) == list:
            subgroup = inkex.etree.SubElement(group, 'g')
            paths_to_group(subpaths,subgroup,style)
        else:
            attribs = { 'style': simplestyle.formatStyle(style), 'd': subpaths}
            inkex.etree.SubElement(group, inkex.addNS('path','svg'), attribs )