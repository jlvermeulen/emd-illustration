import numpy as np
from scipy.optimize import linear_sum_assignment

import geometry, distance

def solve(data, subdivs):
    if all(isinstance(x, geometry.Point) for x in data['sources']):
        if distance.get_metric() == 'L1' and len(data['sinks']) == 1 and isinstance(data['sinks'][0], geometry.Segment) and data['sinks'][0].start.y == data['sinks'][0].end.y:
            return solve_points_to_horizontal_segment_exact(data)

    return solve_general(data, subdivs)

def solve_general(data, subdivs):
    subbed_sources, subbed_sinks = subdivide_input(data, subdivs)

    distances = []
    for source in subbed_sources:
        distances.append(calculate_costs(source, subbed_sinks))

    cost_matrix = np.array(distances)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    flows = []
    for i in range(len(row_ind)):
        flows.append(geometry.Segment(subbed_sources[row_ind[i]].centre(), subbed_sinks[col_ind[i]].centre(), cost_matrix[row_ind[i]][col_ind[i]]))

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows, 'cost': cost_matrix[row_ind, col_ind].sum() / (subdivs + 1) }

def solve_points_to_horizontal_segment_exact(data):
    sink = data['sinks'][0]

    flow_polygons = []
    start = sink.start
    direction = (sink.end - sink.start) / sink.weight

    for source in sorted(data['sources'], key = lambda x: x.x):
        end = start + direction * source.weight
        flow_polygons.append(geometry.Polygon([source, end, start]))
        start = end

    return { 'sources': data['sources'], 'sinks': data['sinks'], 'flows': flow_polygons, 'cost': 0 }

def solve_points_to_horizontal_segment(data, subdivs):
    subbed_sources, subbed_sinks = subdivide_input(data, subdivs)

    flows = []
    claimed = [False] * len(subbed_sinks)
    total_cost = 0
    for source in sorted(data['sources'], key = lambda x: x.x):
        distances = calculate_costs(source, subbed_sinks)

        start = 0
        for i in range(len(subbed_sinks)):
            if not claimed[i]:
                start = i
                break

        n_claimed = 0
        for i in range(start, len(subbed_sinks)):
            if not claimed[i]:
                claimed[i] = True
                n_claimed += 1
                flows.append(geometry.Segment(source.centre(), subbed_sinks[i].centre(), distances[i]))
                total_cost += distances[i]

                if n_claimed == source.weight * (subdivs + 1):
                    break

        if n_claimed < source.weight * (subdivs + 1):
            for i in range(start - 1, -1, -1):
                if not claimed[i]:
                    claimed[i] = True
                    n_claimed += 1
                    flows.append(geometry.Segment(source.centre(), subbed_sinks[i].centre(), distances[i]))
                    total_cost += distances[i]

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows, 'cost': total_cost / (subdivs + 1) }

def subdivide_input(data, subdivs):
    subbed_sources = subdivide(data['sources'], subdivs)
    subbed_sinks   = subdivide(data['sinks'], subdivs)

    if len(subbed_sources) != len(subbed_sinks):
        print('Total weight is not equal, solution may be incomplete.')

    return subbed_sources, subbed_sinks

def subdivide(data, subdivs):
    subbed_data = []

    for dat in data:
        weight_split = dat.subdivide(dat.weight - 1)
        for part in weight_split:
            subbed_data += part.subdivide(subdivs)

    return subbed_data

def calculate_costs(source, sinks):
    return [distance.dist(sink.centre(), source.centre()) for sink in sinks]
