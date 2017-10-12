from point import Point

class Segment:
    def __init__(self, start, end, weight = 1):
        self.start = start
        self.end = end
        self.weight = float(weight)

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.start, self.end, self.weight)

    def centre(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2, self.weight)

    def subdivide(self, subdivs):
        vec = (self.end - self.start) / (subdivs + 1)
        return [Segment(self.start + i * vec, self.start + (i + 1) * vec, self.weight / (subdivs + 1)) for i in range(subdivs + 1)]
