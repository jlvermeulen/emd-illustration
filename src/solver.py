import numpy as np
from scipy.optimize import linear_sum_assignment

import geometry, distance

def solve(data, subdivs):
    if sum(x.weight for x in data['sources']) != sum(x.weight for x in data['sinks']):
        print('Total weight of sources and sinks not equal, solution may be incomplete.')

    if all(isinstance(x, geometry.Point) for x in data['sources']) and all(isinstance(x, geometry.Segment) for x in data['sinks']):
        y = data['sinks'][0].start.y
        if distance.get_metric() == 'L1' and all(x.start.y == y and x.end.y == y for x in data['sinks']):
           return solve_points_to_horizontal_collinear_segments_L1_exact(data)

    return solve_general(data, subdivs)

def solve_general(data, subdivs):
    subbed_sources, subbed_sinks = subdivide_input(data, subdivs)

    distances = []
    for source in subbed_sources:
        distances.append(calculate_distances(source, subbed_sinks))

    cost_matrix = np.array(distances)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    flows = []
    for i in range(len(row_ind)):
        flows.append(geometry.Segment(subbed_sources[row_ind[i]].centre(), subbed_sinks[col_ind[i]].centre(), cost_matrix[row_ind[i]][col_ind[i]]))

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows, 'cost': cost_matrix[row_ind, col_ind].sum() / (subdivs + 1) }

def solve_points_to_horizontal_collinear_segments_L1_exact(data):
    sinks = geometry.resolve_horizontal_segment_overlaps(data['sinks'])
    sorted_sources = sorted(data['sources'], key = lambda x: x.x)

    sink_index = 0
    start = sinks[sink_index].start
    direction = (sinks[sink_index].end - sinks[sink_index].start) / sinks[sink_index].weight

    source_index = 0
    remaining_weight = sorted_sources[source_index].weight

    flow_polygons = []
    while True:
        next_sink, next_source = False, False

        end = start + direction * remaining_weight

        if end.x <= sinks[sink_index].end.x:
            next_source = True

        if end.x >= sinks[sink_index].end.x:
            next_sink = True
            remaining_weight = (end.x - sinks[sink_index].end.x) / direction.x
            end = sinks[sink_index].end

        flow_polygons.append(geometry.Polygon([sorted_sources[source_index], end, start], (end.x - start.x) / (sinks[sink_index].end.x - sinks[sink_index].start.x) * sinks[sink_index].weight))

        start = end

        if next_sink:
            sink_index += 1
            if sink_index == len(sinks):
                break

            start = sinks[sink_index].start
            direction = (sinks[sink_index].end - sinks[sink_index].start) / sinks[sink_index].weight

        if next_source:
            source_index += 1
            if source_index == len(sorted_sources):
                break

            remaining_weight = sorted_sources[source_index].weight

    total_cost = 0
    for poly in flow_polygons:
        source, right, left = poly.vertices
        half_left  = (min(right.x, source.x) + left.x) / 2
        half_right = (right.x + max(left.x, source.x)) / 2
        left_len   = max(0, min(source.x, right.x) - left.x)
        right_len  = max(0, right.x - max(source.x, left.x))
        total_len  = right.x - left.x

        cost  = abs(source.y - right.y)
        cost += (source.x - half_left) * left_len / total_len
        cost += (half_right - source.x) * right_len / total_len

        total_cost += cost * poly.weight

    return { 'sources': data['sources'], 'sinks': data['sinks'], 'flows': flow_polygons, 'cost': total_cost }

def solve_points_to_horizontal_segment_L1(data, subdivs):
    subbed_sources, subbed_sinks = subdivide_input(data, subdivs)

    flows = []
    claimed = [False] * len(subbed_sinks)
    total_cost = 0
    for source in sorted(data['sources'], key = lambda x: x.x):
        distances = calculate_distances(source, subbed_sinks)

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
        print('Number of subdivided sinks and sources not equal, solution may be incomplete.')

    return subbed_sources, subbed_sinks

def subdivide(data, subdivs):
    subbed_data = []

    for dat in data:
        weight_split = dat.subdivide(int(dat.weight) - 1)
        for part in weight_split:
            subbed_data += part.subdivide(subdivs)

    return subbed_data

def calculate_distances(source, sinks):
    return [distance.dist(sink.centre(), source.centre()) for sink in sinks]
