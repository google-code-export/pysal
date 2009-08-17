"""
Computational geometry code for PySAL: Python Spatial Analysis Library.

Authors:
Sergio Rey <srey@asu.edu>
Xinyue Ye <xinyue.ye@gmail.com>
Charles Schmidt <Charles.Schmidt@asu.edu>
Andrew Winslow <Andrew.Winslow@asu.edu>

Not to be used without permission of the authors. 

Style Guide, Follow:
http://www.python.org/dev/peps/pep-0008/


Class comment format:

    Brief class description.

    Attributes:
    attr 1 -- type -- description of attr 1
    attr 2 -- type -- description of attr 2

    Extras (notes, references, examples, doctest, etc.)


Function comment format:

    Brief function description.

    function(arg 1 type, arg 2 type, keyword=keyword arg 3 type) -> return type

    Argument:
    arg 1 -- description of arg 1
    arg 2 -- description of arg 2

    Keyword Arguments:
    arg 3 -- description of arg 3

    Extras (notes, references, examples, doctest, etc.)
"""

__author__  = "Sergio J. Rey, Xinyue Ye, Charles Schmidt, Andrew Winslow"
__credits__ = "Copyright (c) 2005-2009 Sergio J. Rey"

import doctest
import math
import copy
from shapes import *

def get_bounding_box(items):
    """
    Returns the bounding box of a collection of points, rectangles and polygons.

    bounding_box(Point/Rectangle/Polygon list) -> Rectangle

    Arguments:
    items -- a collection of items to compute a bounding box for

    Example:
    >>> bb = get_bounding_box([Point((-1, 5)), Rectangle(0, 6, 11, 12)])
    >>> bb.left
    -1.0
    >>> bb.lower
    5.0
    >>> bb.right
    11.0
    >>> bb.upper
    12.0
    """
    def left(o):
        if hasattr(o, 'bounding_box'): # Polygon, Ellipse
            return o.bounding_box.left
        elif hasattr(o, 'left'): # Rectangle
            return o.left
        else: # Point
            return o[0]

    def right(o):
        if hasattr(o, 'bounding_box'): # Polygon, Ellipse
            return o.bounding_box.right
        elif hasattr(o, 'right'): # Rectangle
            return o.right
        else: # Point
            return o[0]

    def lower(o):
        if hasattr(o, 'bounding_box'): # Polygon, Ellipse
            return o.bounding_box.lower
        elif hasattr(o, 'lower'): # Rectangle
            return o.lower
        else: # Point
            return o[1]

    def upper(o):
        if hasattr(o, 'bounding_box'): # Polygon, Ellipse
            return o.bounding_box.upper
        elif hasattr(o, 'upper'): # Rectangle
            return o.upper
        else: # Point
            return o[1]

    return Rectangle(min(map(left, items)), min(map(lower, items)), max(map(right, items)), max(map(upper, items))) 

def get_angle_between(ray1, ray2):
    """
    Returns the angle formed between a pair of rays which share an origin

    get_angle_between(Ray, Ray) -> number

    Arguments:
    ray1 -- a ray forming the beginning of the angle measured
    ray2 -- a ray forming the end of the angle measured

    Example:
    >>> get_angle_between(Ray(Point((0, 0)), Point((1, 0))), Ray(Point((0, 0)), Point((1, 0)))) 
    0.0
    """
    if ray1.o != ray2.o:
        raise ValueError, 'Rays must have the same origin.'
    vec1 = (ray1.p[0] - ray1.o[0], ray1.p[1] - ray1.o[1])
    vec2 = (ray2.p[0] - ray2.o[0], ray2.p[1] - ray2.o[1])
    rot_theta = -math.atan2(vec1[1], vec1[0])
    rot_matrix = [[math.cos(rot_theta), -math.sin(rot_theta)], [math.sin(rot_theta), math.cos(rot_theta)]]
    rot_vec2 = (rot_matrix[0][0]*vec2[0] + rot_matrix[0][1]*vec2[1], 
                rot_matrix[1][0]*vec2[0] + rot_matrix[1][1]*vec2[1])
    return math.atan2(rot_vec2[1], rot_vec2[0])

def is_collinear(p1, p2, p3):
    """
    Returns whether a triplet of points is collinear.

    is_collinear(Point, Point, Point) -> bool

    Arguments:
    p1 -- a point (Point)
    p2 -- another point (Point)
    p3 -- yet another point (Point)

    Example:
    >>> is_collinear(Point((0, 0)), Point((1, 1)), Point((5, 5)))
    True
    >>> is_collinear(Point((0, 0)), Point((1, 1)), Point((5, 0)))
    False
    """
    return ((p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0]) == 0)

def get_segments_intersect(seg1, seg2):
    """
    Returns the intersection of two segments.

    get_segments_intersect(LineSegment, LineSegment) -> Point

    Arguments:
    seg1 -- a segment to check intersection for
    seg2 -- a segment to check intersection for

    Example:
    >>> seg1 = LineSegment(Point((0, 0)), Point((0, 10)))
    >>> seg2 = LineSegment(Point((-5, 5)), Point((5, 5)))
    >>> i = get_segments_intersect(seg1, seg2)
    >>> isinstance(i, Point)
    True
    >>> str(i)
    '(0.0, 5.0)'
    >>> seg3 = LineSegment(Point((100, 100)), Point((100, 101)))
    >>> i = get_segments_intersect(seg2, seg3)
    """
    p1 = seg1.p1
    p2 = seg1.p2
    p3 = seg2.p1
    p4 = seg2.p2
    a = p2[0] - p1[0]
    b = p3[0] - p4[0]
    c = p2[1] - p1[1]
    d = p3[1] - p4[1]
    det = float(a*d - b*c)
    if det == 0:
        return None
    a_inv = d/det
    b_inv = -b/det
    c_inv = -c/det
    d_inv = a/det
    m = p3[0] - p1[0]
    n = p3[1] - p1[1]
    x = a_inv*m + b_inv*n
    y = c_inv*m + d_inv*n
    intersect_exists = 0 <= x <= 1 and 0 <= y <= 1
    if not intersect_exists:
        return None
    return Point((p1[0] + x*(p2[0] - p1[0]), p1[1] + x*(p2[1] - p1[1])))
    
def get_segment_point_intersect(seg, pt):
    """
    Returns the intersection of a segment and point.

    get_segment_point_intersect(LineSegment, Point) -> Point

    Arguments:
    seg -- a segment to check intersection for
    pt -- a point to check intersection for

    Example:
    >>> seg = LineSegment(Point((0, 0)), Point((0, 10)))
    >>> pt = Point((0, 5))
    >>> i = get_segment_point_intersect(seg, pt)
    >>> str(i)
    '(0.0, 5.0)'
    >>> pt2 = Point((5, 5))
    >>> get_segment_point_intersect(seg, pt2)  
    """
    vec1 = (pt[0] - seg.p1[0], pt[1] - seg.p1[1])
    vec2 = (seg.p2[0] - seg.p1[0], seg.p2[1] - seg.p1[1])
    if (vec1[0]*vec2[1] - vec1[1]*vec2[0]) == 0:
        return pt
    return None 

def get_polygon_point_intersect(poly, pt):
    """
    Returns the intersection of a polygon and point.

    get_polygon_point_intersect(Polygon, Point) -> Point

    Arguments:
    poly -- a polygon to check intersection for
    pt -- a point to check intersection for

    Example:
    >>> poly = Polygon([Point((0, 0)), Point((1, 0)), Point((1, 1)), Point((0, 1))])
    >>> pt = Point((0.5, 0.5))
    >>> i = get_polygon_point_intersect(poly, pt)
    >>> str(i)
    '(0.5, 0.5)'
    >>> pt2 = Point((2, 2))
    >>> get_polygon_point_intersect(poly, pt2)
    """
    def pt_lies_on_part_boundary(pt, vertices):
        return filter(lambda i: get_segment_point_dist(LineSegment(vertices[i], vertices[i+1]), pt)[0] == 0,
                      xrange(-1, len(vertices)-1)) != []

    def pt_in_part(pt, vertices):
        vert_y_set = set([v[1] for v in vertices])
        while pt[1] in vert_y_set:
            pt = (pt[0], pt[1] + -1e-14 + random.random()*2e-14) # Perturb the location very slightly
        inters = 0
        for i in xrange(-1, len(vertices)-1):
            v1 = vertices[i]
            v2 = vertices[i+1]
            if get_segments_intersect(LineSegment(v1, v2), LineSegment((min([pt[0], v1[0], v2[0]]) - 1, pt[1]), pt)) != None:
                inters += 1
        return inters % 2 == 1
    
    if poly._holes != [[]]:
        raise NotImplementedError, 'Cannot compute containment for polygon with holes'
    if get_rectangle_point_intersect(poly.bounding_box, pt) == None: # Weed out points that aren't even close
        return None
    if filter(lambda verts: pt_lies_on_part_boundary(pt, verts), poly._vertices) != []:
        return pt
    if filter(lambda verts: pt_in_part(pt, verts), poly._vertices) != []:
        return pt
    return None
    
def get_rectangle_point_intersect(rect, pt):
    """
    Returns the intersection of a rectangle and point.

    get_rectangle_point_intersect(Rectangle, Point) -> Point

    Arguments:
    rect -- a rectangle to check intersection for
    pt -- a point to check intersection for

    Example:
    >>> rect = Rectangle(0, 0, 5, 5)
    >>> pt = Point((1, 1))
    >>> i = get_rectangle_point_intersect(rect, pt)
    >>> str(i)
    '(1.0, 1.0)'
    >>> pt2 = Point((10, 10))
    >>> get_rectangle_point_intersect(rect, pt2)
    """
    if rect.left <= pt[0] <= rect.right and rect.lower <= pt[1] <= rect.upper:
        return pt  
    return None

def get_ray_segment_intersect(ray, seg):
    """
    Returns the intersection of a ray and line segment.

    get_ray_segment_intersect(Ray, Point) -> Point or LineSegment

    Arguments:
    ray -- a ray to check intersection for
    seg -- a line segment to check intersection for

    Example:
    >>> ray = Ray(Point((0, 0)), Point((0, 1)))
    >>> seg = LineSegment(Point((-1, 10)), Point((1, 10)))
    >>> i = get_ray_segment_intersect(ray, seg)
    >>> isinstance(i, Point)
    True
    >>> str(i)
    '(0.0, 10.0)'
    >>> seg2 = LineSegment(Point((10, 10)), Point((10, 11)))
    >>> get_ray_segment_intersect(ray, seg2)
    """
    d = max(math.hypot(seg.p1[0] - ray.o[0], seg.p1[1] - ray.o[1]), 
            math.hypot(seg.p2[0] - ray.o[0], seg.p2[1] - ray.o[1])) + 1 # Upper bound on origin to segment dist (+1)
    ratio = d/math.hypot(ray.o[0] - ray.p[0], ray.o[1] - ray.p[1])
    ray_seg = LineSegment(ray.o, Point((ray.o[0] + ratio*(ray.p[0] - ray.o[0]), 
                                        ray.o[1] + ratio*(ray.p[1] - ray.o[1]))))
    return get_segments_intersect(seg, ray_seg)

def get_polygon_point_dist(poly, pt):
    """
    Returns the distance between a polygon and point.

    get_polygon_point_dist(Polygon, Point) -> number

    Arguments:
    poly -- a polygon to compute distance from
    pt -- a point to compute distance from

    Example:
    >>> poly = Polygon([Point((0, 0)), Point((1, 0)), Point((1, 1)), Point((0, 1))])
    >>> pt = Point((2, 0.5))
    >>> get_polygon_point_dist(poly, pt)
    1.0
    >>> pt2 = Point((0.5, 0.5))
    >>> get_polygon_point_dist(poly, pt2) 
    0.0
    """
    if get_polygon_point_intersect(poly, pt) != None:
        return 0.0
    part_prox = []
    for vertices in poly._vertices:
        part_prox.append(min([get_segment_point_dist(LineSegment(vertices[i], vertices[i+1]), pt)[0] 
                              for i in xrange(-1, len(vertices)-1)]))
    return min(part_prox)

def get_points_dist(pt1, pt2):
    """
    Returns the distance between a pair of points.

    get_points_dist(Point, Point) -> number

    Arguments:
    pt1 -- a point
    pt2 -- the other point
   
    Example:
    >>> get_points_dist(Point((4, 4)), Point((4, 8)))
    4.0
    >>> get_points_dist(Point((0, 0)), Point((0, 0)))
    0.0
    """
    return math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])

def get_segment_point_dist(seg, pt):
    """
    Returns the distance between a line segment and point and distance along the segment of the closest
    point on the segment to the point as a ratio of the length of the segment.

    get_segment_point_dist(LineSegment, Point) -> (number, number)

    Arguments:
    seg -- a line segment to compute distance from
    pt -- a point to compute distance from

    Example:
    >>> seg = LineSegment(Point((0, 0)), Point((10, 0)))
    >>> pt = Point((5, 5))
    >>> get_segment_point_dist(seg, pt)
    (5.0, 0.5)
    >>> pt2 = Point((0, 0))
    >>> get_segment_point_dist(seg, pt2)
    (0.0, 0.0)
    """
    src_p = seg.p1
    dest_p = seg.p2

    # Shift line to go through origin
    points_0 = pt[0] - src_p[0]
    points_1 = pt[1] - src_p[1]
    points_2 = 0
    points_3 = 0
    points_4 = dest_p[0] - src_p[0]
    points_5 = dest_p[1] - src_p[1]

    segment_length = get_points_dist(src_p, dest_p)

    # Meh, robustness...maybe should incorporate this into a more general
    # approach later
    if segment_length == 0:
        return (get_points_dist(pt, src_p), 0)

    u_x = points_4/segment_length
    u_y = points_5/segment_length

    inter_x = u_x*u_x*points_0 + u_x*u_y*points_1
    inter_y = u_x*u_y*points_0 + u_y*u_y*points_1

    src_proj_dist = get_points_dist((0,0), (inter_x, inter_y))
    dest_proj_dist = get_points_dist((inter_x, inter_y), (points_4, points_5))

    if src_proj_dist > segment_length or dest_proj_dist > segment_length:
        src_pt_dist = get_points_dist((points_2, points_3), (points_0, points_1))
        dest_pt_dist = get_points_dist((points_4, points_5), (points_0, points_1))
        if src_pt_dist < dest_pt_dist:
            return (src_pt_dist, 0)
        else:
            return (dest_pt_dist, 1)
    else:
        return (get_points_dist((inter_x, inter_y), (points_0, points_1)), src_proj_dist/segment_length)

def get_point_at_angle_and_dist(ray, angle, dist):
    """
    Returns the point at a distance and angle relative to the origin of a ray.

    get_point_at_angle_and_dist(Ray, number, number) -> Point

    Arguments:
    ray -- the ray which the angle and distance are relative to
    angle -- the angle relative to the ray at which the point is located
    dist -- the distance from the ray origin at which the point is located

    Example:
    >>> ray = Ray(Point((0, 0)), Point((1, 0)))
    >>> pt = get_point_at_angle_and_dist(ray, math.pi, 1.0)
    >>> isinstance(pt, Point)
    True
    >>> round(pt[0], 8)
    -1.0
    >>> round(pt[1], 8)
    0.0
    """
    v = (ray.p[0] - ray.o[0], ray.p[1] - ray.o[1])
    cur_angle = math.atan2(v[1],v[0])
    dest_angle = cur_angle + angle
    return Point((ray.o[0] + dist*math.cos(dest_angle), ray.o[1] + dist*math.sin(dest_angle)))

def convex_hull(points):
    """
    Returns the convex hull of a set of points.

    convex_hull(Point list) -> Polygon

    Arguments:
    points -- a list of points to compute the convex hull for

    Example:
    >>> points = [Point((0, 0)), Point((4, 4)), Point((4, 0)), Point((3, 1))]
    >>> convex_hull(points)
    [(0.0, 0.0), (4.0, 0.0), (4.0, 4.0)]
    """
    points = copy.copy(points)
    lowest = min(points, key=lambda p: (p[1], p[0]))

    points.remove(lowest)
    points.sort(key=lambda p: math.atan2(p[1] - lowest[1], p[0] - lowest[0]))

    stack = [lowest]   

    def right_turn(p1, p2, p3):
        # Returns if p1 -> p2 -> p3 forms a 'right turn'
        vec1 = (p2[0] - p1[0], p2[1] - p1[1])
        vec2 = (p3[0] - p2[0], p3[1] - p2[1])
        return vec2[0]*vec1[1] - vec2[1]*vec1[0] >= 0

    for p in points:
        stack.append(p)
        while len(stack) > 3 and right_turn(stack[-3], stack[-2], stack[-1]):
            stack.pop(-2) 
   
    return stack 

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()




