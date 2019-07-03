#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Origami Patterns plugin

Inkscape extension that creates origami tesselation patterns, create for the Origabot project

'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import os          # here for alternative debug method only - so not usually required
import Origami_Patterns.helpers as hp
import Origami_Patterns.Waterbomb as Waterbomb
import Origami_Patterns.Kresling as Kresling

__version__ = '0.2'

inkex.localize()

class OrigamiPatterns(inkex.Effect): 
    
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
                                     dest="pattern", default="waterbomb",
                                     help="Origami pattern")      
        
        self.OptionParser.add_option("-l", "--lines",
                                     action="store", type="int",
                                     dest="lines", default=8,
                                     help="Number of lines")
        
        self.OptionParser.add_option("-c", "--columns",
                                     action="store", type="int", 
                                     dest="columns", default=16,
                                     help="Number of columns")


        self.OptionParser.add_option("", "--ratio",
                                     action="store", type="float", 
                                     dest="ratio", default=1,
                                     help="Angle ratio")

        self.OptionParser.add_option("", "--length",
                                     action="store", type="float", 
                                     dest="length", default=10.0,
                                     help="Length of grid square")

        
        self.OptionParser.add_option('', '--bool1', action = 'store',
                                     type = 'inkbool', dest = 'bool1',
                                     default = True,
                                     help = 'Bool 1.')

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

        self.OptionParser.add_option('-v', '--valley_stroke_color', action = 'store',
                                     type = 'string', dest = 'valley_stroke_color',
                                     default = 65535, # Blue
                                     help = 'The valley creases color.')
        self.OptionParser.add_option('', '--valley_stroke_width', action = 'store',
                                     type = 'float', dest = 'valley_stroke_width',
                                     default = 0.1,
                                     help = 'Width of valley strokes.')
        self.OptionParser.add_option('', '--valley_dashes_number', action = 'store',
                                     type = 'float', dest = 'valley_dashes_number',
                                     default = 6,
                                     help = 'Dashes per length unit.')
        self.OptionParser.add_option('', '--valley_dashes_bool', action = 'store',
                                     type = 'inkbool', dest = 'valley_dashes_bool',
                                     default = True,
                                     help = 'Dashed strokes?.')

        self.OptionParser.add_option('-m', '--mountain_stroke_color', action = 'store',
                                     type = 'string', dest = 'mountain_stroke_color',
                                     default = 4278190335, # Red
                                     help = 'The mountain creases color.')
        self.OptionParser.add_option('', '--mountain_stroke_width', action = 'store',
                                     type = 'float', dest = 'mountain_stroke_width',
                                     default = 0.1,
                                     help = 'Width of mountain strokes.')
        self.OptionParser.add_option('', '--mountain_dashes_number', action = 'store',
                                     type = 'float', dest = 'mountain_dashes_number',
                                     default = 6,
                                     help = 'Dashes per length unit.')
        self.OptionParser.add_option('', '--mountain_dashes_bool', action = 'store',
                                     type = 'inkbool', dest = 'mountain_dashes_bool',
                                     default = True,
                                     help = 'Dashed strokes?.')

        self.OptionParser.add_option('-e', '--enclosure_stroke_color', action = 'store',
                                     type = 'string', dest = 'enclosure_stroke_color',
                                     default = 255, # Black
                                     help = 'The mountain creases color.')
        self.OptionParser.add_option('', '--enclosure_stroke_width', action = 'store',
                                     type = 'float', dest = 'enclosure_stroke_width',
                                     default = 0.1,
                                     help = 'Width of enclosure strokes.')
        self.OptionParser.add_option('', '--enclosure_dashes_number', action = 'store',
                                     type = 'float', dest = 'enclosure_dashes_number',
                                     default = 6,
                                     help = 'Dashes per length unit.')
        self.OptionParser.add_option('', '--enclosure_dashes_bool', action = 'store',
                                     type = 'inkbool', dest = 'enclosure_dashes_bool',
                                     default = False,
                                     help = 'Dashed strokes?.')

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

    def create_styles_dict(self):
        """ Create styles dictionary.
            - 
        """
        
        # define colour and stroke widt
        mountain_style = {  'stroke': self.getColorString(self.options.mountain_stroke_color), 
                            'fill': 'none',  
                            'stroke-width': self.options.mountain_stroke_width}
        valley_style = {    'stroke': self.getColorString(self.options.valley_stroke_color), 
                            'fill': 'none',  
                            'stroke-width': self.options.valley_stroke_width}
        enclosure_style = { 'stroke': self.getColorString(self.options.enclosure_stroke_color), 
                            'fill': 'none',  
                            'stroke-width': self.options.enclosure_stroke_width}

        # check if dashed option selected
        if(self.options.mountain_dashes_bool): 
            mountain_style['stroke-dasharray'] = (self.options.length/2)/self.options.mountain_dashes_number
        if(self.options.valley_dashes_bool): 
            valley_style['stroke-dasharray'] = (self.options.length/2)/self.options.valley_dashes_number
        if(self.options.enclosure_dashes_bool): 
            enclosure_style['stroke-dasharray'] = (self.options.length/2)/self.options.enclosure_dashes_number

        self.styles_dict = {'m' : mountain_style,
                            'v' : valley_style,
                            'e' : enclosure_style}

    """ Select pattern and create.
            - 
        """
    def create_pattern(self):
        # basic_options = [self.options.lines,self.options.columns,self.options.length]
        
        if(self.options.pattern == 'waterbomb' or self.options.pattern == 'magic_ball'):
            self.pattern = Waterbomb.Waterbomb(self.options.lines,self.options.columns,self.options.length,phase_shift=self.options.bool1,waterbomb_type = self.options.pattern)
        elif(self.options.pattern == 'kresling'):
            self.pattern = Kresling.Kresling(self.options.lines,self.options.columns,self.options.lengths,self.options.ratio)
        elif(self.options.pattern == 'kresling_radial'):
            self.pattern = Kresling.Kresling_radial(self.options.lines,self.options.columns,self.options.length,self.options.ratio,min_polygon=self.options.bool1)


### -------------------------------------------------------------------
### This is your main function and is called when the extension is run.
    
    def effect(self):
        # ~ accuracy = self.options.accuracy
        # ~ unit_factor = self.calc_unit_factor()
        # what page are we on
        # page_id = self.options.active_tab # sometimes wrong the very first time
        
        # This finds center of current view in inkscape
        # t = 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] )
        t = 'translate(%s,%s)' % (0, 0 )
        g_attribs = { inkex.addNS('label','inkscape'): '{} Origami pattern'.format(self.options.pattern),
                    #   inkex.addNS('transform-center-x','inkscape'): str(-bbox_center[0]),
                    #   inkex.addNS('transform-center-y','inkscape'): str(-bbox_center[1]),
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t}
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        
        # get paths for selected origami pattern
        self.create_pattern()

        # construct dictionary containing styles
        self.create_styles_dict()

        self.pattern.draw_path_tree(topgroup,self.styles_dict)
        
if __name__ == '__main__':
    e = OrigamiPatterns()
    e.affect()

# Notes
