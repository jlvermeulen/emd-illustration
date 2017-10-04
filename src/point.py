from math import sqrt

class Point:
    def __init__(self, x, y, weight = 0):
        self.x = float(x)
        self.y = float(y)
        self.weight = float(weight)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.weight)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.weight)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.weight)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other, self.weight)

    def __neg__(self):
        return Point(-self.x, -self.y, self.weight)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return not self <= other

    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return sqrt(self.length_squared())

    def centre(self):
        return self

    def subdivide(self, subdivs):
        return [Point(self.x, self.y, self.weight / (subdivs + 1)) for i in range(subdivs + 1)]
