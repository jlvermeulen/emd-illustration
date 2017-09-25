from point import Point

class Segment:
    def __init__(self, start, end, weight = 0):
        if not isinstance(start, Point):
            raise TypeError('start must be a Point')
        if not isinstance(end, Point):
            raise TypeError('end must be a Point')

        self.start = start
        self.end = end
        self.weight = float(weight)

    def centre(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2, self.weight)

    def subdivide(self, subdivs):
        vec = (self.end - self.start) / (subdivs + 1)
        return [Segment(self.start + i * vec, self.start + (i + 1) * vec, self.weight / (subdivs + 1)) for i in range(subdivs + 1)]
