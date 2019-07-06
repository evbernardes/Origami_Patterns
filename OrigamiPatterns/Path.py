"""
Path Class

Defines a path and what it is supposed to be (mountain, valley, edge)

"""


class Path:
    """ Class that defines an svg stroke to be drawn in Inkscape

    Attributes
    ---------
    points: list of 2D tuples
        stroke will connect all points
    style: str
        Single character defining style of stroke. Default values are:
        'm' for mountain creases
        'v' for valley creases
        'e' for edge borders
    path: str
        svg compliant string defining stoke lines
    """

    def __init__(self, points, style, closed=False, inverse=False):
        """ Constructor

        Parameters
        ---------
        points: list of 2D tuples
            stroke will connect all points
        style: str
            Single character defining style of stroke. Default values are:
            'm' for mountain creases
            'v' for valley creases
            'e' for edge borders
        closed: bool 
            if true, last point will be connected to first point at the end
        inverse: bool
            if true, stroke will start at the last point and go all the way to the first one
        """
        self.points = points
        self.style = style
        self.closed = closed
        self.inverse = inverse
        self._generate_path()

    @classmethod
    def generate_hgrid(cls, xlims, ylims, nb_of_divisions, style, include_edge=False):
        """ Generate list of Path instances, in which each Path is a stroke defining
        a horizontal grid dividing the space xlims * ylims nb_of_divisions times.

        All lines are alternated, to minimize Laser Cutter unnecessary movements

        Parameters
        ---------
        xlims: tuple
            Defines x_min and x_max for space that must be divided.
        ylims: tuple
            Defines y_min and y_max for space that must be divided.
        nb_of_divisions: int
            Defines how many times it should be divided.
        style: str
            Single character defining style of stroke.
        include_edge: bool 
            Defines if edge should be drawn or not.

        Returns
        ---------
        paths: list of Path instances
        """
        rect_len = (ylims[1] - ylims[0])/nb_of_divisions
        hgrid = []
        for i in range(1 - include_edge, nb_of_divisions + include_edge):
            hgrid.append(Path([(xlims[0], ylims[0]+i*rect_len),
                               (xlims[1], ylims[0]+i*rect_len)],
                              style=style, inverse=i % 2 == 0))
        return hgrid

    @classmethod
    def generate_vgrid(cls, xlims, ylims, nb_of_divisions, style, include_edge=False):
        """ Generate list of Path instances, in which each Path is a stroke defining
        a vertical grid dividing the space xlims * ylims nb_of_divisions times.

        All lines are alternated, to minimize Laser Cutter unnecessary movements

        Parameters
        ---------
        -> refer to generate_hgrid

        Returns
        ---------
        paths: list of Path instances
        """
        rect_len = (xlims[1] - xlims[0])/nb_of_divisions
        vgrid = []
        for i in range(1 - include_edge, nb_of_divisions + include_edge):
            vgrid.append(Path([(xlims[0]+i*rect_len, ylims[0]),
                               (xlims[0]+i*rect_len, ylims[1])],
                              style=style, inverse=i % 2 == 0))
        return vgrid

    @classmethod
    def generate_separated_paths(cls, points, style, closed=False):
        """ Generate list of Path instances, in which each Path is the stroke
        between each two point tuples, in case each stroke must be handled separately.

        Returns
        ---------
        paths: list of Path instances
        """
        paths = []
        for i in range(len(points) - 1 + int(closed)):
            j = (i+1)%len(points)
            paths.append(cls([points[i], points[j]],
                             style))
        return paths

    def __add__(self, offset):
        """ " + " operator overload.
        Adding a tuple to a Path returns a new path with all points having an offset
        defined by the tuple
        """
        if type(offset) != tuple:
            inkex.errormsg(_("Paths can only be added by tuples"))
            raise TypeError("Paths can only be added by tuples")
        points_new = []
        for point in self.points:
            points_new.append([(point[0]+offset[0]),
                              (point[1]+offset[1])])

        return Path(points_new, self.style, self.closed, self.inverse)

    def _generate_path(self):
        """ Generate svg line string defining stroke, called by the constructor
        """
        self.path = ''
        if self.inverse:
            points = self.points[::-1]
        else:
            points = self.points
        for i in range(len(points)-1):
            self.path = self.path+'M{},{}L{},{}'.format(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
        if self.closed:
            self.path = self.path+'M{},{}L{},{}z'.format(points[-1][0], points[-1][1], points[0][0], points[0][1])
