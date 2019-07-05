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
        self._generate_path(closed, inverse)

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
            paths.append(cls([points[i],points[j]],
                             style))
        return paths

    def _generate_path(self, closed, inverse):
        """ Generate svg compliant string defining stroke, called by the constructor
        """
        self.path = ''
        if inverse:
            points = self.points[::-1]
        else:
            points = self.points
        for i in range(len(points)-1):
            self.path = self.path+'M{},{}L{},{}'.format(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
        if closed:
            self.path = self.path+'M{},{}L{},{}z'.format(points[-1][0], points[-1][1], points[0][0], points[0][1])
