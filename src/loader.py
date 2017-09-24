import os.path
import json

import geometry

def load(pathname):
    if not os.path.isfile(pathname):
        return

    with open(pathname, 'r') as file:
        return json.load(file, object_hook = parse_object)

def parse_object(dic):
    if 'type' in dic:
        t = dic['type']
        if t == 'point':
            return geometry.Point(dic['x'], dic['y'])
        if t == 'segment':
            return geometry.Segment(dic['start'], dic['end'])
    else:
        return dic
