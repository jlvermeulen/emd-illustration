from point import Point
from segment import Segment
from polygon import Polygon

def supporting_line_intersection(seg1, seg2):
    diff1 = seg1.start - seg1.end
    diff2 = seg2.start - seg2.end

    denom = cross(diff1, diff2)
    if abs(denom) < 1e-3:
        return False

    cross1 = cross(seg1.start, seg1.end)
    cross2 = cross(seg2.start, seg2.end)

    num1 = cross1 * diff2.x - diff1.x * cross2
    num2 = cross1 * diff2.y - diff1.y * cross2

    return Point(num1 / denom, num2 / denom)

def cross(p1, p2):
    return p1.x * p2.y - p1.y * p2.x

def resolve_horizontal_segment_overlaps(segments):
    y = segments[0].start.y

    interval_points = []
    for seg in segments:
        interval_points.append((seg.start.x, seg.weight / abs(seg.start.x - seg.end.x), seg.start.x < seg.end.x))
        interval_points.append((seg.end.x, seg.weight / abs(seg.start.x - seg.end.x), seg.end.x < seg.start.x))

    new_segments = []
    last = (None, 0)
    for point in sorted(interval_points):
        if point[2]:
            if last[1] > 0:
                new_segments.append(Segment(Point(last[0], y), Point(point[0], y), last[1] * (point[0] - last[0])))
            last = (point[0], last[1] + point[1])
        else:
            new_segments.append(Segment(Point(last[0], y), Point(point[0], y), last[1] * (point[0] - last[0])))
            last = (point[0], last[1] - point[1])

    return new_segments
