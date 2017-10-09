import geometry

dist = None

def switch_metric(metric):
    global dist
    dist = distance_metrics[metric]

def get_metric():
    for name, metric in distance_metrics.items():
        if metric == dist:
            return name

def dist_L1(p1, p2):
    diff = p1 - p2
    return abs(diff.x) + abs(diff.y) + dist_L2(p1, p2) / 1000000

def dist_L2(p1, p2):
    diff = p1 - p2
    return diff.length()

def dist_Linf(p1, p2):
    diff = p1 - p2
    return max(abs(diff.x), abs(diff.y)) + dist_L2(p1, p2) / 1000000

distance_metrics = {
    'L1': dist_L1,
    'L2': dist_L2,
    'L∞': dist_Linf
}
