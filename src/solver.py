import numpy as np
from scipy.optimize import linear_sum_assignment

import geometry

def solve(data, subdivs):
    subbed_sources, subbed_sinks = subdivide(data['sources'], data['sinks'], subdivs)
    cost_matrix = []
    for source in subbed_sources:
        cost_matrix.append(calculate_costs(source, subbed_sinks))

    row_ind, col_ind = linear_sum_assignment(np.array(cost_matrix))

    flows = []
    for i in range(len(row_ind)):
        flows.append((subbed_sources[row_ind[i]], subbed_sinks[col_ind[i]]))

    return { 'sources': subbed_sources, 'sinks': subbed_sinks, 'flows': flows }

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
