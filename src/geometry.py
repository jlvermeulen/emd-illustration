from point import Point
from segment import Segment

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
