import json

import geometry

def load(filename):
    with open(filename, 'r') as file:
        return json.load(file, object_hook = parse_object)

def parse_object(dic):
    if 'type' in dic:
        t = dic['type']
        if t == 'point':
            return geometry.Point(dic['x'], dic['y'], dic['weight'] if 'weight' in dic else 1)
        if t == 'segment':
            return geometry.Segment(dic['start'], dic['end'], dic['weight'] if 'weight' in dic else 1)
        if t == 'flow':
            return geometry.Segment(dic['from'], dic['to'], 0)
    else:
        return dic
