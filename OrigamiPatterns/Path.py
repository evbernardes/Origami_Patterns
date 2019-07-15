"""
Path Class

Defines a path and what it is supposed to be (mountain, valley, edge)

"""
import inkex

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
            points_new.append((point[0]+offset[0],
                               point[1]+offset[1]))

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

    def __mul__(self, transform):
        """ " * " operator overload.
        Define multiplication of a Path to a vector in complex exponential representation

        Parameters
        ---------
        transform: float of tuple of length 2 or 4
            if float, transform represents magnitude
                Example: path * 3
            if tuple length 2, transform[0] represents magnitude and transform[1] represents angle of rotation
                Example: path * (3, pi)
            if tuple length 4, transform[2],transform[3] define a different axis of rotation
                Example: path * (3, pi, 1, 1)
        """
        points_new = []

        if isinstance(transform, (int, long, float)):
            for p in self.points:
                points_new.append([(transform * p[0],
                                    transform * p[0])])

        elif isinstance(transform, (list, tuple)):
            if len(transform) == 2:
                u = transform[0]*cos(transform[1])
                v = transform[0]*sin(transform[1])
                x_, y_ = 0, 0
            elif len(transform) == 4:
                u = transform[0]*cos(transform[1])
                v = transform[0]*sin(transform[1])
                x_, y_ = transform[2:]
            else:
                raise IndexError('Paths can only be multiplied by a number or a tuple/list of length 2 or 4')

            for p in self.points:
                x, y = p[0]-x_, p[1]-y_
                points_new.append((x_ + x * u - y * v,
                                   y_ + x * v + y * u))

        else:
            raise TypeError('Paths can only be multiplied by a number or a tuple/list of length 2 or 4')

        return Path(points_new, self.style, self.closed)

    @classmethod
    def list_rotate(cls, paths, theta, translation=(0, 0)):
        """ Generate list of new Path instances, rotation each path by transform

        Parameters
        ---------
        paths: Path or list
            list of N Path instances
        theta: float (radians)
            angle of rotation
        translation: tuple or list 2
            axis of rotation

        Returns
        ---------
        paths_new: list
            list of N Path instances
        """
        if len(translation) != 2:
            TypeError("Translation must have length 2")

        if type(paths) == Path:
            paths = [paths]

        paths_new = []
        for path in paths:
            paths_new.append(path*(1, theta, translation[0], translation[1]))

        return paths_new

    # TODO:
    # Apparently it's not working properly, must be debugged and tested
    def __div__(self, points):
        """ " / " operator overload.
        Define division of a Path to a list or tuple of length 4 each as reflection:
        path / [(x1, y1, x2, y2)] finds line passing through points (x1,y1) and (x1,y1) and reflects path over it
        """
        if len(points) != 4:
            TypeError("Paths can only be divided by list or tuple of length 4")

        (x1, y1, x2, y2) = points

        if x1 == x2 and y1 == y2:
            ValueError("Duplicate points don't define a line")
        elif x1 == x2:
            t_x = [-1, 0, 2*x1, 1]
            t_y = [0, 1, 0, 1]
        else:
            m = (y2 - y1)/(x2 - x1)
            t = y1 - m*x1
            t_x = [1 - m**2, 2*m, -2*m*t, m**2 + 1]
            t_y = [2*m, m**2 - 1, +2*t, m**2 + 1]

        points_new = []
        for p in self.points:
            x_ = (t_x[0]*p[0] + t_x[1]*p[1] + t_x[2]) / t_x[3]
            y_ = (t_y[0]*p[0] + t_y[1]*p[1] + t_y[2]) / t_y[3]
            points_new.append((x_, y_))

        return Path(points_new, self.style, self.closed)

    # TODO:
    # Apparently it's not working properly, must be debugged and tested
    @classmethod
    def list_reflect(cls, paths, p1, p2):
        """ Generate list of new Path instances, rotation each path by transform

        Parameters
        ---------
        paths: Path or list
            list of N Path instances
        p1: tuple or list of size 2
        p2: tuple or list of size 2

        Returns
        ---------
        paths_new: list
            list of N Path instances
        """

        if type(paths) == Path:
            paths = [paths]

        paths_new = []
        for path in paths:
            paths_new.append(path / (p1[0], p1[0], p2[0], p2[1]))

        return paths_new

