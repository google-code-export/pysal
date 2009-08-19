import random

class Triangle:
    """
    Representation of a triangle. 
    The representation is valuable for its numerical stability.

    Attributes:
    v1 -- a vertex of the triangle (number 2-tuple)
    v2 -- a vertex of the triangle (number 2-tuple)
    v3 -- a vertex of the triangle (number 2-tuple)
    """

    def __init__(self, v1, v2, v3):
        """
        Create a triangle with the specified vertices.

        Test tag: <tc>#is#Triangle.__init__</tc>

        __init__((number, number), (number, number), (number, number)) -> Triangle

        Arguments:
        v1 -- a vertex of the triangle
        v2 -- a vertex of the triangle
        v3 -- a vertex of the triangle

        Example:
        >>> t = Triangle(Point((0, 0)), Point((1, 0)), Point((0, 1)))
        """
        cross_prod = ((v2[0] - v1[0])*(v3[1] - v1[1]) - 
                      (v2[1] - v1[1])*(v3[0] - v1[0]))
        if cross_prod == 0:
            raise ArithmeticError, 'Triangle vertices cannot be collinear.'
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    @property
    def cw(self):
        """
        Test tag: <tc>#is#Triangle.cw</tc>
 
        Returns whether the vertices of the triangle are in clockwise order.

        cw() -> bool

        Example:
        >>> Triangle(Point((0, 0)), Point((0, 1)), Point((1, 0))).cw
        True
        >>> Triangle(Point((0, 0)), Point((1, 0)), Point((0, 1))).cw
        False
        """
        cross_prod = ((self.v2[0] - self.v1[0])*(self.v3[1] - self.v1[1]) -
                      (self.v2[1] - self.v1[1])*(self.v3[0] - self.v1[0]))
        if cross_prod > 0:
            return False
        else:
            return True

    def contains(self, pt):
        """
        Returns whether a location lies inside or outside the triangle.

        Test tag: <tc>#is#Triangle.contains</tc>

        contains(Point) -> bool

        Arguments:
        loc -- a location which lies inside or outside the triangle

        Example:
        >>> Triangle(Point((0, 0)), Point((1, 0)), Point((0, 1))).contains(Point((2, 2)))
        False
        >>> Triangle(Point((0, 0)), Point((1, 0)), Point((0, 1))).contains(Point((0.1, 0.1)))
        True
        """
        if self.cw:
            v1 = self.v1
            v2 = self.v2
            v3 = self.v3
        else:
            v1 = self.v1
            v2 = self.v3
            v3 = self.v2
        tvec1 = (v2[0] - v1[0], v2[1] - v1[1])
        tvec2 = (v3[0] - v2[0], v3[1] - v2[1])
        tvec3 = (v1[0] - v3[0], v1[1] - v3[1])
        lvec1 = (pt[0] - v1[0], pt[1] - v1[1])
        lvec2 = (pt[0] - v2[0], pt[1] - v2[1])
        lvec3 = (pt[0] - v3[0], pt[1] - v3[1])
        cross_prod1 = lvec1[0]*tvec1[1] - lvec1[1]*tvec1[0]
        cross_prod2 = lvec2[0]*tvec2[1] - lvec2[1]*tvec2[0]
        cross_prod3 = lvec3[0]*tvec3[1] - lvec3[1]*tvec3[0]
        return cross_prod1 > 0 and cross_prod2 > 0 and cross_prod3 > 0

def collinear_pts(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1]) - 
            (p2[1] - p1[1])*(p3[0] - p1[0]) == 0)

def neg_ray_intersect(p1, p2, p3):
    # Returns whether a ray in the negative-x direction from p3 intersects the segment between 
    if not min(p1[1], p2[1]) <= p3[1] <= max(p1[1], p2[1]):
        return False
    if p1[1] > p2[1]:
        vec1 = (p2[0] - p1[0], p2[1] - p1[1])
    else:
        vec1 = (p1[0] - p2[0], p1[1] - p2[1])
    vec2 = (p3[0] - p1[0], p3[1] - p1[1])
    return vec1[0]*vec2[1] - vec2[0]*vec1[1] >= 0

def loc_in_polygon(loc, vertices):
    vert_y_set = set([v[1] for v in vertices])
    while loc[1] in vert_y_set:
        loc = (loc[0], loc[1] + -1e-14 + random.random()*2e-14) # Perturb the location very slightly
    inters = 0
    for i in xrange(-1, len(vertices)-1):
        v1 = vertices[i]
        v2 = vertices[i+1]
        if neg_ray_intersect(v1, v2, loc):
            inters += 1

    return inters % 2 == 1

def clockwise(vertices):
    """
    Returns a list of the vertices in clockwise order.
    """
    def remove_duplicates(vertices):
        clean = []
        prev = None
        for i in xrange(len(vertices)):
            if vertices[i] != prev:
                clean.append(vertices[i])
            prev = vertices[i]
        return clean

    nondup_verts = remove_duplicates(vertices) # Non-duplicate pts 
    for i in xrange(1, len(nondup_verts)-1):
        if collinear_pts(nondup_verts[i-1], nondup_verts[i], nondup_verts[i+1]):
            continue
        tri = Triangle(nondup_verts[i-1], nondup_verts[i], nondup_verts[i+1])
        if len(filter(lambda v: tri.contains(v), nondup_verts)) == 0:
            in_tri_pt = ((tri.v1[0] + tri.v2[0] +tri.v3[0])/3.0, (tri.v1[1] + tri.v2[1] + tri.v3[1])/3.0)
            if loc_in_polygon(in_tri_pt, nondup_verts):
                if tri.cw:
                    return True
                else:
                    return False#vertices[::-1]
            else:
                if tri.cw:
                    return False#vertices[::-1]
                else:
                    return True#vertices
    raise ArithmeticError, 'Polygon vertices are all collinear'

def main():
    v = [(-106.57798, 35.174143999999998), (-106.583412, 35.174141999999996), (-106.58417999999999, 35.174143000000001), (-106.58377999999999, 35.175542999999998), (-106.58287999999999, 35.180543), (-106.58263099999999, 35.181455), (-106.58257999999999, 35.181643000000001), (-106.58198299999999, 35.184615000000001), (-106.58148, 35.187242999999995), (-106.58127999999999, 35.188243), (-106.58138, 35.188243), (-106.58108, 35.189442999999997), (-106.58104, 35.189644000000001), (-106.58028, 35.193442999999995), (-106.580029, 35.194541000000001), (-106.57974399999999, 35.195785999999998), (-106.579475, 35.196961999999999), (-106.57922699999999, 35.198042999999998), (-106.578397, 35.201665999999996), (-106.57827999999999, 35.201642999999997), (-106.57737999999999, 35.201642999999997), (-106.57697999999999, 35.201543000000001), (-106.56436599999999, 35.200311999999997), (-106.56058, 35.199942999999998), (-106.56048, 35.197342999999996), (-106.56048, 35.195842999999996), (-106.56048, 35.194342999999996), (-106.56048, 35.193142999999999), (-106.56048, 35.191873999999999), (-106.56048, 35.191742999999995), (-106.56048, 35.190242999999995), (-106.56037999999999, 35.188642999999999), (-106.56037999999999, 35.187242999999995), (-106.56037999999999, 35.186842999999996), (-106.56037999999999, 35.186552999999996), (-106.56037999999999, 35.185842999999998), (-106.56037999999999, 35.184443000000002), (-106.56037999999999, 35.182943000000002), (-106.56037999999999, 35.181342999999998), (-106.56037999999999, 35.180433000000001), (-106.56037999999999, 35.179943000000002), (-106.56037999999999, 35.178542999999998), (-106.56037999999999, 35.177790999999999), (-106.56037999999999, 35.177143999999998), (-106.56037999999999, 35.175643999999998), (-106.56037999999999, 35.174444000000001), (-106.56037999999999, 35.174043999999995), (-106.560526, 35.174043999999995), (-106.56478, 35.174043999999995), (-106.56627999999999, 35.174143999999998), (-106.566541, 35.174144999999996), (-106.569023, 35.174157000000001), (-106.56917199999999, 35.174157999999998), (-106.56938, 35.174143999999998), (-106.57061499999999, 35.174143999999998), (-106.57097999999999, 35.174143999999998), (-106.57679999999999, 35.174143999999998), (-106.57798, 35.174143999999998)]

    test = [clockwise(v) for i in xrange(10000)]
    print test.count(True)
    print test.count(False)

if __name__=='__main__':
    import cProfile
    cProfile.run('main()')
