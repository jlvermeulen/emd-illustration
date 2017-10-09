import point, segment

class Polygon:
    def __init__(self, verts, weight = 1):
        self.vertices = verts
        self.weight = weight

    def __repr__(self):
        return str(self.vertices)
