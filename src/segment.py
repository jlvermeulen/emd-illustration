from point import Point

class Segment:
    def __init__(self, start, end):
        if not isinstance(start, Point):
            raise TypeError('start must be a Point')
        if not isinstance(end, Point):
            raise TypeError('end must be a Point')

        self.start = start
        self.end = end
