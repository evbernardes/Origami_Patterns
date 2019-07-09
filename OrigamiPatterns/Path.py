"""
Path Class

Defines a path and what it is supposed to be (mountain, valley, edge)

"""
from math import sin,cos


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

    def __init__(self, points, style, closed=False, invert=False):
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
        invert: bool
            if true, stroke will start at the last point and go all the way to the first one
        """
        self.points = points
        self.style = style
        self.closed = closed

        if invert:
            self.points = points[::-1]
        else:
            self.points = points

        self._generate_path()

    def _generate_path(self):
        """ Generate svg line string defining stroke, called by the constructor
        """
        self.path = ''
        points = self.points
        for i in range(len(points)-1):
            self.path = self.path+'M{},{}L{},{}'.format(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
        if self.closed:
            self.path = self.path+'M{},{}L{},{}z'.format(points[-1][0], points[-1][1], points[0][0], points[0][1])

    def invert(self):
        """ Inverts path
        """

        self.points = self.points[::-1]
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
            hgrid.append(cls([(xlims[0], ylims[0]+i*rect_len),
                              (xlims[1], ylims[0]+i*rect_len)],
                             style=style, invert=i % 2 == 0))
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
            vgrid.append(cls([(xlims[0]+i*rect_len, ylims[0]),
                              (xlims[0]+i*rect_len, ylims[1])],
                             style=style, invert=i % 2 == 0))
        return vgrid

    @classmethod
    def generate_separated_paths(cls, points, styles, closed=False):
        """ Generate list of Path instances, in which each Path is the stroke
        between each two point tuples, in case each stroke must be handled separately.

        Returns
        ---------
        paths: list
            list of Path instances
        """
        paths = []
        if type(styles) == str:
            styles = [styles] * (len(points) - 1 + int(closed))
        elif len(styles) != len(points) - 1 + int(closed):
            raise TypeError("Number of paths and styles don't match")
        for i in range(len(points) - 1 + int(closed)):
            j = (i+1)%len(points)
            paths.append(cls([points[i], points[j]],
                             styles[i]))
        return paths

    def __add__(self, offsets):
        """ " + " operator overload.
        Adding a tuple to a Path returns a new path with all points having an offset
        defined by the tuple
        """
        if type(offsets) == list:
            if len(offsets) != 1 or len(offsets) != len(self.points):
                raise TypeError("Paths can only be added by a tuple of a list of N tuples, "
                                "where N is the same number of points")

        elif type(offsets) != tuple:
            raise TypeError("Paths can only be added by tuples")
        else:
            offsets = [offsets] * len(self.points)

        points_new = []
        for point, offset in zip(self.points, offsets):
            points_new.append([(point[0]+offset[0]),
                               (point[1]+offset[1])])

        return Path(points_new, self.style, self.closed)

    @classmethod
    def list_add(cls, paths, offsets):
        """ Generate list of new Path instances, adding a different tuple for each list

        Parameters
        ---------
        paths: Path or list
            list of N Path instances
        offsets: tuple or list
            list of N tuples

        Returns
        ---------
        paths_new: list
            list of N Path instances
        """
        if type(paths) == Path and type(offsets) == tuple:
            paths = [paths]
            offsets = [offsets]
        elif type(paths) == list and type(offsets) == tuple:
            offsets = [offsets] * len(paths)
        elif type(paths) == Path and type(offsets) == list:
            paths = [paths] * len(offsets)
        elif type(paths) == list and type(offsets) == list:
            if len(paths) == 1:
                paths = [paths[0]] * len(offsets)
            elif len(offsets) == 1:
                offsets = [offsets[0]] * len(paths)
            elif len(offsets) != len(paths):
                raise TypeError("List of paths and list of tuples must have same length. {} paths and {} offsets "
                                " where given".format(len(paths), len(offsets)))
            else:
                pass

        paths_new = []
        for path, offset in zip(paths, offsets):
            paths_new.append(path+offset)

        return paths_new

