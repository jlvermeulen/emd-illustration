import json

import geometry

def export(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, cls = GeometryEncoder)

class GeometryEncoder(json.JSONEncoder):
    def default(self, obj):
        dic = obj.__dict__
        if isinstance(obj, geometry.Point):
            dic['type'] = 'point'
        elif isinstance(obj, geometry.Segment):
            dic['type'] = 'segment'
        else:
            raise TypeError
        return dic
