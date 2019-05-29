#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Example of extensions template for inkscape

'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import os          # here for alternative debug method only - so not usually required
# many other useful ones in extensions folder. E.g. simplepath, cubicsuperpath, ...

from math import cos, sin, radians

__version__ = '0.2'

inkex.localize()

### Your helper functions go here
def create_magic_ball(lines,columns,length):
    
    # create grid
    x_grid = [[i,length*i/2.] for i in range(0,2*columns + 1)]  # each element is [i,x(i)]
    y_grid = [[i,length*i/2.] for i in range(0,2*lines + 1)]    # each element is [i,y(i)]

    # create points
    points = []
    for y in zip(*y_grid)[1]:
        points.append([(x,y) for x in zip(*x_grid)[1]])
    
    # create a list for the horizontal creases and another for the vertical creases
    # alternate strokes to minimize laser cutter path
    mountain_path_h = []
    for y in y_grid[2:-1:2]:
        if y[0] % 4 == 0:		
            mountain_path_h.append(points_to_path([(x_grid[-1][1],y[1]),(x_grid[0][1],y[1])]))
        else:
            mountain_path_h.append(points_to_path([(x_grid[0][1],y[1]),(x_grid[-1][1],y[1])]))
    mountain_path_v = []
    for x in x_grid[1:-1:1]:
        if x[0] % 2 == 0:
            mountain_path_v.append(points_to_path([(x[1],y_grid[-1][1]),(x[1],y_grid[0][1])]))
            # inkex.debug(str(mountain_path_v))
        else:
            mountain_path_v.append(points_to_path([(x[1],y_grid[0][1]),(x[1],y_grid[-1][1])]))
    mountains = [mountain_path_h,mountain_path_v]
    
    # create a list for valley creases
    valleys = []
    for y in y_grid[1:-1:2]:
        
        if ((y[0] + 1)/2)%2 == 0:
            top_points = [(x_grid[0][1],y_grid[y[0]-1][1])]
            for i in range(1,len(x_grid),2):  # even lines (X's), upper half
                if ((i+2)/2) % 2 == 1:
                    top_points.append((x_grid[i][1],y_grid[y[0]][1]))
                    top_points.append((x_grid[i+1][1],y_grid[y[0]+1][1]))
                else:
                    top_points.append((x_grid[i][1],y_grid[y[0]][1]))
                    top_points.append((x_grid[i+1][1],y_grid[y[0]-1][1]))

            if ((len(x_grid)+2)/2) % 2 == 0:
                bottom_points = [(x_grid[-1][1],y_grid[y[0]-1][1])]
            else:
                bottom_points = [(x_grid[-1][1],y_grid[y[0]+1][1])]
            for i in range(len(x_grid)-2,0,-2):  # even lines (X's), bottom half
                if ((i+1)/2) % 2 == 1:
                    bottom_points.append((x_grid[i][1],y_grid[y[0]][1]))
                    bottom_points.append((x_grid[i-1][1],y_grid[y[0]+1][1]))
                else:
                    bottom_points.append((x_grid[i][1],y_grid[y[0]][1]))
                    bottom_points.append((x_grid[i-1][1],y_grid[y[0]-1][1]))

            valleys.append([points_to_path(top_points),points_to_path(bottom_points)])
            
        else:
            top_points = [(x_grid[0][1],y_grid[y[0]][1])]
            for i in range(1,len(x_grid)):  # odd lines (losanges), upper half
                if i % 2 == 0:
                    top_points.append((x_grid[i][1],y_grid[y[0]][1]))
                else:
                    top_points.append((x_grid[i][1],y_grid[y[0]-1][1]))

            bottom_points = []    
            for i in range(len(x_grid)-1,0,-1): # odd lines (losanges), bottom half
                if i % 2 == 0:
                    bottom_points.append((x_grid[i][1],y_grid[y[0]][1]))
                else:
                    bottom_points.append((x_grid[i][1],y_grid[y[0]+1][1]))
            bottom_points.append((x_grid[0][1],y_grid[y[0]][1]))

            valleys.append([points_to_path(top_points),points_to_path(bottom_points)])

        


	
    # create a list for enclosure strokes
    enclosures = []
    enclosures.append(points_to_path([  (x_grid[0][1],y_grid[0][1]),    # left
                                        (x_grid[0][1],y_grid[-1][1])]))

    enclosures.append(points_to_path([  (x_grid[-1][1],y_grid[0][1]),   # right
                                        (x_grid[-1][1],y_grid[-1][1])]))

    enclosures.append(points_to_path([  (x_grid[0][1],y_grid[0][1]),    # top
                                        (x_grid[-1][1],y_grid[0][1])]))

    enclosures.append(points_to_path([  (x_grid[0][1],y_grid[-1][1]),   # bottom
                                        (x_grid[-1][1],y_grid[-1][1])]))
    
	
    return points,mountains,valleys,enclosures

def points_to_path(points,closed=False):
    path = ''
    for i in range(len(points)-1):
        path = path+'M{},{}L{},{}'.format(points[i][0],points[i][1],points[i+1][0],points[i+1][1])
    if closed:
        path = path+'M{},{}L{},{}z'.format(points[-1][0],points[-1][1],points[0][0],points[0][1])
    return path

def paths_to_group(paths,group,style):
    for subpaths in paths:
        if type(subpaths) == list:
            subgroup = inkex.etree.SubElement(group, 'g')
            paths_to_group(subpaths,subgroup,style)
        else:
            attribs = { 'style': simplestyle.formatStyle(style), 'd': subpaths}
            inkex.etree.SubElement(group, inkex.addNS('path','svg'), attribs )

class OrigamiGridPatterns(inkex.Effect): 
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__
            
        # Define your list of parameters defined in the .inx file
        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="magic_ball",
                                     help="Origami pattern")      
        
        self.OptionParser.add_option("-l", "--lines",
                                     action="store", type="int",
                                     dest="lines", default=8,
                                     help="Number of lines")
        
        self.OptionParser.add_option("-c", "--columns",
                                     action="store", type="int", 
                                     dest="columns", default=16,
                                     help="Number of columns")

        self.OptionParser.add_option("", "--length",
                                     action="store", type="float", 
                                     dest="length", default=10.0,
                                     help="Length of grid square")

        self.OptionParser.add_option("-u", "--units",
                                     action="store", type="string",
                                     dest="units", default='mm',
                                     help="Units this dialog is using")
                                     
        # self.OptionParser.add_option("-a", "--add_attachment",
        #                              action="store", type="inkbool", 
        #                              dest="add_attachment", default=False,
        #                              help="command line help")

        self.OptionParser.add_option("", "--accuracy", # note no cli shortcut
                                     action="store", type="int",
                                     dest="accuracy", default=0,
                                     help="command line help")
        self.OptionParser.add_option('-v', '--valleyColor', action = 'store',
                                     type = 'string', dest = 'valleyColor',
                                     default = 65535, # Blue
                                     help = 'The valley creases color.')
        self.OptionParser.add_option('-m', '--mountainColor', action = 'store',
                                     type = 'string', dest = 'mountainColor',
                                     default = 4278190335, # Red
                                     help = 'The mountain creases color.')
        self.OptionParser.add_option('-e', '--enclosureColor', action = 'store',
                                     type = 'string', dest = 'enclosureColor',
                                     default = 16711935, # Green
                                     help = 'The mountain creases color.')
        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
    def getUnittouu(self, param):
        " for 0.48 and 0.91 compatibility "
        try:
            return inkex.unittouu(param)
        except AttributeError:
            return self.unittouu(param)
            
    def getColorString(self, longColor, verbose=False):
        """ Convert the long into a #RRGGBB color value
            - verbose=true pops up value for us in defaults
            conversion back is A + B*256^1 + G*256^2 + R*256^3
        """
        if verbose: inkex.debug("%s ="%(longColor))
        longColor = long(longColor)
        if longColor <0: longColor = long(longColor) & 0xFFFFFFFF
        hexColor = hex(longColor)[2:-3]
        hexColor = '#' + hexColor.rjust(6, '0').upper()
        if verbose: inkex.debug("  %s for color default value"%(hexColor))
        return hexColor
    
    def add_text(self, node, text, position, text_height=12):
        """ Create and insert a single line of text into the svg under node.
        """
        line_style = {'font-size': '%dpx' % text_height, 'font-style':'normal', 'font-weight': 'normal',
                     'fill': '#F6921E', 'font-family': 'Bitstream Vera Sans,sans-serif',
                     'text-anchor': 'middle', 'text-align': 'center'}
        line_attribs = {inkex.addNS('label','inkscape'): 'Annotation',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(position[0]),
                       'y': str((position[1] + text_height) * 1.2)
                       }
        line = inkex.etree.SubElement(node, inkex.addNS('text','svg'), line_attribs)
        line.text = text

           
    def calc_unit_factor(self):
        """ return the scale factor for all dimension conversions.
            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        unit_factor = self.getUnittouu(str(1.0) + self.options.units)
        return unit_factor



### -------------------------------------------------------------------
### This is your main function and is called when the extension is run.
    
    def effect(self):
        """ Calculate Gear factors from inputs.
            - Make list of radii, angles, and centers for each tooth and 
              iterate through them
            - Turn on other visual features e.g. cross, rack, annotations, etc
        """
        valley_stroke_color = self.getColorString(self.options.valleyColor)
        mountain_stroke_color = self.getColorString(self.options.mountainColor)
        enclosure_stroke_color = self.getColorString(self.options.enclosureColor)
        # gather incoming params and convert
        lines = self.options.lines
        columns = self.options.columns
        length = self.options.length
        # ~ accuracy = self.options.accuracy
        # ~ unit_factor = self.calc_unit_factor()
        # what page are we on
        page_id = self.options.active_tab # sometimes wrong the very first time
        
        # This finds center of current view in inkscape
        t = 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] )
        t = 'translate(%s,%s)' % (0, 0 )
        g_attribs = { inkex.addNS('label','inkscape'): '({},{}){} Origami pattern'.format(lines,columns,self.options.pattern),
                    #   inkex.addNS('transform-center-x','inkscape'): str(-bbox_center[0]),
                    #   inkex.addNS('transform-center-y','inkscape'): str(-bbox_center[1]),
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t}
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        
        # get paths for selected origami pattern
        points,mountains,valleys,enclosures = create_magic_ball(lines,columns,length)
        
        # Create mountain group and add them to top group
        mountain_style = { 'stroke': mountain_stroke_color, 'fill': 'none', 'stroke-width': 0.1 }
        mountain_group = inkex.etree.SubElement(topgroup, 'g')
        paths_to_group(mountains,mountain_group,mountain_style)
        
        # Create valley group and add them to top group
        valley_style = { 'stroke': valley_stroke_color, 'fill': 'none', 'stroke-width': 0.1 }
        valley_group = inkex.etree.SubElement(topgroup, 'g')
        paths_to_group(valleys,valley_group,valley_style)
        
        # Create enclosure group and add them to top group
        enclosure_style = { 'stroke': enclosure_stroke_color, 'fill': 'none', 'stroke-width': 0.2 }
        enclosure_group = inkex.etree.SubElement(topgroup, 'g')
        paths_to_group(enclosures,enclosure_group,enclosure_style)
        
        
if __name__ == '__main__':
    e = OrigamiGridPatterns()
    e.affect()

# Notes

