#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper functions

"""
import os
from abc import abstractmethod

import inkex       # Required
import simplestyle # will be needed here for styles support

from Path import Path



class Pattern(inkex.Effect):
    """ Class that inherits inkex.Effect and further specializes it for different
    Patterns generation

    Attributes
    ---------
    styles_dict: dict
            defines styles for every possible stroke. Default values are:
            styles_dict = {'m' : mountain_style,
                           'v' : valley_style,
                           'e' : edge_style}

    topgroup: inkex.etree.SubElement
            Top Inkscape group element 

    path_tree: nested list 
        Contains "tree" of Path instances, defining new groups for each
        sublist

    translate: 2 sized tuple
        Defines translation to be added when drawing to Inkscape (default: 0,0)
    """
    
    @abstractmethod
    def generate_path_tree(self):
        """ Generate nested list of Path instances 
        Abstract method, must be defined in all child classes
        """
        pass

    @abstractmethod
    def __init__(self):
        """ Parse all common options 
        
        Must be reimplemented in child classes to parse specialized options
        """

        inkex.Effect.__init__(self)  # initialize the super class
        
        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__

        self.OptionParser.add_option("-u", "--units",
                                     action="store", type="string",
                                     dest="units", default='mm',
                                     help="Units this dialog is using")
                                     
        # self.OptionParser.add_option("-a", "--add_attachment",
        #                              action="store", type="inkbool", 
        #                              dest="add_attachment", default=False,
        #                              help="command line help")

        # self.OptionParser.add_option("", "--accuracy", # note no cli shortcut
        #                              action="store", type="int",
        #                              dest="accuracy", default=0,
        #                              help="command line help")

        # --------------------------------------------------------------------------------------------------------------
        # mountain options
        self.OptionParser.add_option('-m', '--mountain_stroke_color', action='store',
                                     type='string', dest='mountain_stroke_color',
                                     default=4278190335,  # Red
                                     help='The mountain creases color.')
        self.OptionParser.add_option('', '--mountain_stroke_width', action='store',
                                     type='float', dest='mountain_stroke_width',
                                     default=0.1,
                                     help='Width of mountain strokes.')
        self.OptionParser.add_option('', '--mountain_dashes_len', action='store',
                                     type='float', dest='mountain_dashes_len',
                                     default=1.0,
                                     help='Mountain dash + gap length.')
        self.OptionParser.add_option('', '--mountain_dashes_duty', action='store',
                                     type='float', dest='mountain_dashes_duty',
                                     default=0.5,
                                     help='Mountain dash duty cycle.')
        self.OptionParser.add_option('', '--mountain_dashes_bool', action='store',
                                     type='inkbool', dest='mountain_dashes_bool',
                                     default=True,
                                     help='Dashed strokes?.')

        # --------------------------------------------------------------------------------------------------------------
        # valley options
        self.OptionParser.add_option('-v', '--valley_stroke_color', action='store',
                                     type='string', dest='valley_stroke_color',
                                     default=65535,  # Blue
                                     help='The valley creases color.')
        self.OptionParser.add_option('', '--valley_stroke_width', action='store',
                                     type='float', dest='valley_stroke_width',
                                     default=0.1,
                                     help='Width of valley strokes.')
        self.OptionParser.add_option('', '--valley_dashes_len', action='store',
                                     type='float', dest='valley_dashes_len',
                                     default=1.0,
                                     help='Valley dash + gap length.')
        self.OptionParser.add_option('', '--valley_dashes_duty', action='store',
                                     type='float', dest='valley_dashes_duty',
                                     default=0.25,
                                     help='Valley dash duty cycle.')
        self.OptionParser.add_option('', '--valley_dashes_bool', action='store',
                                     type='inkbool', dest='valley_dashes_bool',
                                     default=True,
                                     help='Dashed strokes?.')

        # --------------------------------------------------------------------------------------------------------------
        # edge options
        self.OptionParser.add_option('-e', '--edge_stroke_color', action='store',
                                     type='string', dest='edge_stroke_color',
                                     default=255,  # Black
                                     help='The mountain creases color.')
        self.OptionParser.add_option('', '--edge_stroke_width', action='store',
                                     type='float', dest='edge_stroke_width',
                                     default=0.1,
                                     help='Width of edge strokes.')
        self.OptionParser.add_option('', '--edge_dashes_len', action='store',
                                     type='float', dest='edge_dashes_len',
                                     default=1.0,
                                     help='Edge dash + gap length.')
        self.OptionParser.add_option('', '--edge_dashes_duty', action='store',
                                     type='float', dest='edge_dashes_duty',
                                     default=0.25,
                                     help='Edge dash duty cycle.')
        self.OptionParser.add_option('', '--edge_dashes_bool', action='store',
                                     type='inkbool', dest='edge_dashes_bool',
                                     default=False,
                                     help='Dashed strokes?.')

        # --------------------------------------------------------------------------------------------------------------
        # universal crease options
        self.OptionParser.add_option('', '--universal_stroke_color', action='store',
                                     type='string', dest='universal_stroke_color',
                                     default=4278255615,  # Magenta
                                     help='The universal creases color.')
        self.OptionParser.add_option('', '--universal_stroke_width', action='store',
                                     type='float', dest='universal_stroke_width',
                                     default=0.1,
                                     help='Width of universal strokes.')
        self.OptionParser.add_option('', '--universal_dashes_len', action='store',
                                     type='float', dest='universal_dashes_len',
                                     default=1.0,
                                     help='Universal dash + gap length.')
        self.OptionParser.add_option('', '--universal_dashes_duty', action='store',
                                     type='float', dest='universal_dashes_duty',
                                     default=0.25,
                                     help='Universal dash duty cycle.')
        self.OptionParser.add_option('', '--universal_dashes_bool', action='store',
                                     type='inkbool', dest='universal_dashes_bool',
                                     default=False,
                                     help='Dashed strokes?.')

        # --------------------------------------------------------------------------------------------------------------
        # semicrease options
        self.OptionParser.add_option('', '--semicrease_stroke_color', action='store',
                                     type='string', dest='semicrease_stroke_color',
                                     default=4294902015,  # Yellow
                                     help='The semicrease creases color.')
        self.OptionParser.add_option('', '--semicrease_stroke_width', action='store',
                                     type='float', dest='semicrease_stroke_width',
                                     default=0.1,
                                     help='Width of semicrease strokes.')
        self.OptionParser.add_option('', '--semicrease_dashes_len', action='store',
                                     type='float', dest='semicrease_dashes_len',
                                     default=1.0,
                                     help='Semicrease dash + gap length.')
        self.OptionParser.add_option('', '--semicrease_dashes_duty', action='store',
                                     type='float', dest='semicrease_dashes_duty',
                                     default=0.25,
                                     help='Semicrease dash duty cycle.')
        self.OptionParser.add_option('', '--semicrease_dashes_bool', action='store',
                                     type='inkbool', dest='semicrease_dashes_bool',
                                     default=False,
                                     help='Dashed strokes?.')

        # --------------------------------------------------------------------------------------------------------------
        # cut options
        self.OptionParser.add_option('', '--cut_stroke_color', action='store',
                                     type='string', dest='cut_stroke_color',
                                     default=16711935,  # Green
                                     help='The cut creases color.')
        self.OptionParser.add_option('', '--cut_stroke_width', action='store',
                                     type='float', dest='cut_stroke_width',
                                     default=0.1,
                                     help='Width of cut strokes.')
        self.OptionParser.add_option('', '--cut_dashes_len', action='store',
                                     type='float', dest='cut_dashes_len',
                                     default=1.0,
                                     help='Cut dash + gap length.')
        self.OptionParser.add_option('', '--cut_dashes_duty', action='store',
                                     type='float', dest='cut_dashes_duty',
                                     default=0.25,
                                     help='Cut dash duty cycle.')
        self.OptionParser.add_option('', '--cut_dashes_bool', action='store',
                                     type='inkbool', dest='cut_dashes_bool',
                                     default=False,
                                     help='Dashed strokes?.')

        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title',  # use a legitimate default
                                     help="Active tab.")

        self.path_tree = []
        self.translate = (0, 0)
    
    """ 
    Draw path recursively
    - Static method
    - Draws strokes defined on "path_tree" to "group"
    - Inputs:
    -- path_tree [nested list] of Path instances
    -- group [inkex.etree.SubElement]
    -- styles_dict [dict] containing all styles for path_tree
    """
    @staticmethod
    def draw_paths_recursively(path_tree, group, styles_dict):
        """ Static method, draw list of Path instances recursively
        """
        for subpath in path_tree:
            if type(subpath) == list:
                subgroup = inkex.etree.SubElement(group, 'g')
                Pattern.draw_paths_recursively(subpath, subgroup, styles_dict)
            else:
                if subpath.type == 'linear':

                    points = subpath.points
                    path = 'M{},{}'.format(*points[0])
                    for i in range(1, len(points)):
                        path = path + 'L{},{}'.format(*points[i])
                    if subpath.closed:
                        path = path + 'z'

                    attribs = {'style': simplestyle.formatStyle(styles_dict[subpath.style]), 'd': path}
                    inkex.etree.SubElement(group, inkex.addNS('path', 'svg'), attribs )
                else:
                    attribs = {'style': simplestyle.formatStyle(styles_dict[subpath.style]),
                               'cx': str(subpath.points[0][0]), 'cy': str(subpath.points[0][1]),
                               'r': str(subpath.radius)}
                    inkex.etree.SubElement(group, inkex.addNS('circle', 'svg'), attribs )
    
    def effect(self):
        """ Main function 
        
        This is your main function and is called when the extension is run
        """
        # construct dictionary containing styles
        self.create_styles_dict()

        # get paths for selected origami pattern
        self.generate_path_tree()

        # ~ accuracy = self.options.accuracy
        # ~ unit_factor = self.calc_unit_factor()
        # what page are we on
        # page_id = self.options.active_tab # sometimes wrong the very first time

        # Translate according to translate attribute
        g_attribs = {inkex.addNS('label', 'inkscape'): '{} Origami pattern'.format(self.options.pattern),
                       # inkex.addNS('transform-center-x','inkscape'): str(-bbox_center[0]),
                       # inkex.addNS('transform-center-y','inkscape'): str(-bbox_center[1]),
                     inkex.addNS('transform-center-x', 'inkscape'): str(0),
                     inkex.addNS('transform-center-y', 'inkscape'): str(0),
                     'transform': 'translate(%s,%s)' % self.translate}
        # add the group to the document's current layer
        self.topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        self.draw_paths_recursively(self.path_tree, self.topgroup, self.styles_dict)

    def create_styles_dict(self):
        """ Get stroke style parameters and use them to create the styles dictionnary.
        """
        
        # define colour and stroke width
        mountain_style = {'stroke': self.getColorString(self.options.mountain_stroke_color),
                          'fill': 'none',
                          'stroke-width': self.options.mountain_stroke_width}

        valley_style = {'stroke': self.getColorString(self.options.valley_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.valley_stroke_width}

        universal_style = {'stroke': self.getColorString(self.options.universal_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.universal_stroke_width}

        semicrease_style = {'stroke': self.getColorString(self.options.semicrease_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.semicrease_stroke_width}

        cut_style = {'stroke': self.getColorString(self.options.cut_stroke_color),
                        'fill': 'none',
                        'stroke-width': self.options.cut_stroke_width}

        edge_style = {'stroke': self.getColorString(self.options.edge_stroke_color),
                      'fill': 'none',
                      'stroke-width': self.options.edge_stroke_width}

        # check if dashed option selected
        if self.options.mountain_dashes_bool:
            dash = self.options.mountain_dashes_len*self.options.mountain_dashes_duty
            gap = dash - self.options.mountain_dashes_len
            mountain_style['stroke-dasharray'] = "{} {}".format(dash, gap)
        if self.options.valley_dashes_bool:
            dash = self.options.valley_dashes_len * self.options.valley_dashes_duty
            gap = dash - self.options.valley_dashes_len
            valley_style['stroke-dasharray'] = "{} {}".format(dash, gap)
        if self.options.edge_dashes_bool:
            dash = self.options.edge_dashes_len * self.options.edge_dashes_duty
            gap = dash - self.options.edge_dashes_len
            edge_style['stroke-dasharray'] = "{} {}".format(dash, gap)
        if self.options.universal_dashes_bool:
            dash = self.options.universal_dashes_len * self.options.universal_dashes_duty
            gap = dash - self.options.universal_dashes_len
            universal_style['stroke-dasharray'] = "{} {}".format(dash, gap)
        if self.options.semicrease_dashes_bool:
            dash = self.options.semicrease_dashes_len * self.options.semicrease_dashes_duty
            gap = dash - self.options.semicrease_dashes_len
            semicrease_style['stroke-dasharray'] = "{} {}".format(dash, gap)
        if self.options.cut_dashes_bool:
            dash = self.options.cut_dashes_len * self.options.cut_dashes_duty
            gap = dash - self.options.cut_dashes_len
            cut_style['stroke-dasharray'] = "{} {}".format(dash, gap)

        self.styles_dict = {'m': mountain_style,
                            'v': valley_style,
                            'u': universal_style,
                            's': semicrease_style,
                            'c': cut_style,
                            'e': edge_style}
    
    def getUnittouu(self, param):
        """ for 0.48 and 0.91 compatibility
        """
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
    



