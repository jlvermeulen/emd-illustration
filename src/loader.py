import json

import geometry

def load(pathname):
    with open(pathname, 'r') as file:
        return json.load(file, object_hook = parse_object)

def parse_object(dic):
    if 'type' in dic:
        t = dic['type']
        if t == 'point':
            return geometry.Point(dic['x'], dic['y'], dic['weight'] if 'weight' in dic else 0)
        if t == 'segment':
            if dic['start'].weight > 0 or dic['end'].weight > 0:
                print('Warning: weights of segment endpoints will be ignored.')
            return geometry.Segment(dic['start'], dic['end'], dic['weight'])
    else:
        return dic
