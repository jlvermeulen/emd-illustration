import numpy as np
from scipy.optimize import linear_sum_assignment

import geometry, distance

def solve(data, subdivs):
    subbed_sources = subdivide(data['sources'], subdivs)
    subbed_sinks   = subdivide(data['sinks'], subdivs)

    if len(subbed_sources) != len(subbed_sinks):
        print('Total weight is not equal, solution may be incomplete.')

    distances = []
    for source in subbed_sources:
        distances.append(calculate_costs(source, subbed_sinks))

    cost_matrix = np.array(distances)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    flows = []
    for i in range(len(row_ind)):
        flows.append(geometry.Segment(subbed_sources[row_ind[i]].centre(), subbed_sinks[col_ind[i]].centre(), cost_matrix[row_ind[i]][col_ind[i]]))

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows, 'cost': cost_matrix[row_ind, col_ind].sum() / (subdivs + 1) }

def subdivide(data, subdivs):
    subbed_data = []

    for dat in data:
        weight_split = dat.subdivide(dat.weight - 1)
        for part in weight_split:
            subbed_data += part.subdivide(subdivs)

    return subbed_data

def calculate_costs(source, sinks):
    return [distance.dist(sink.centre(), source.centre()) for sink in sinks]
