import numpy as np
from scipy.optimize import linear_sum_assignment

import geometry

def solve(data, subdivs):
    subbed_sources, subbed_sinks = subdivide(data['sources'], data['sinks'], subdivs)
    distances = []
    for source in subbed_sources:
        distances.append(calculate_costs(source, subbed_sinks))

    cost_matrix = np.array(distances)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    flows = []
    for i in range(len(row_ind)):
        flows.append(geometry.Segment(subbed_sources[row_ind[i]].centre(), subbed_sinks[col_ind[i]].centre(), cost_matrix[row_ind[i]][col_ind[i]]))

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows, 'cost': cost_matrix[row_ind, col_ind].sum() / (subdivs + 1) }

def subdivide(sources, sinks, subdivs):
    subbed_sources = []
    subbed_sinks   = []

    for source in sources:
        subbed_sources += source.subdivide(subdivs)
    for sink in sinks:
        subbed_sinks += sink.subdivide(subdivs)

    return subbed_sources, subbed_sinks

def calculate_costs(source, sinks):
    return [(sink.centre() - source.centre()).length() for sink in sinks]
