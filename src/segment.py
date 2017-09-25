from point import Point

class Segment:
    def __init__(self, start, end, weight):
        if not isinstance(start, Point):
            raise TypeError('start must be a Point')
        if not isinstance(end, Point):
            raise TypeError('end must be a Point')

        self.start = start
        self.end = end
        self.weight = float(weight)

    def centre(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2, 0)

    def subdivide(self):
        return (Segment(self.start, self.centre(), self.weight / 2), Segment(self.centre(), self.end, self.weight / 2))
