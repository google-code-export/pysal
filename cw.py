from pysal.cg import Triangle
import random
def collinear_pts(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1]) - 
            (p2[1] - p1[1])*(p3[0] - p1[0]) == 0)

def segments_intersect(p1,p2,p3,p4):
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
    # Inclusive...hoping this is an ok assumption
    # Also have a little margin built in for rounding errors...
    # tendancy is towards intersection
    intersect_exists = -1e-10 <= x <= 1+1e-10 and -1e-10 <= y <= 1 + 1e-10
    if not intersect_exists:
        return None
    return (p1[0] + x*(p2[0] - p1[0]), p1[1] + x*(p2[1] - p1[1]))

def loc_in_polygon(loc, vertices):
    vert_y_set = set([v[1] for v in vertices])
    while loc[1] in vert_y_set:
        loc = (loc[0], loc[1] + -1e-14 + random.random()*2e-14) # Perturb the location very slightly
    
    inters = 0
    for i in xrange(-1, len(vertices)-1):
        v1 = vertices[i]
        v2 = vertices[i+1]
        if segments_intersect(v1, v2, (min([loc[0], v1[0], v2[0]]) - 1, loc[1]), loc) != None:
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
                    return False 
            else:
                if tri.cw:
                    return False
                else:
                    return True
    raise ArithmeticError, 'Polygon vertices are all collinear'

if __name__=='__main__':
    v = [(-106.57798, 35.174143999999998), (-106.583412, 35.174141999999996), (-106.58417999999999, 35.174143000000001), (-106.58377999999999, 35.175542999999998), (-106.58287999999999, 35.180543), (-106.58263099999999, 35.181455), (-106.58257999999999, 35.181643000000001), (-106.58198299999999, 35.184615000000001), (-106.58148, 35.187242999999995), (-106.58127999999999, 35.188243), (-106.58138, 35.188243), (-106.58108, 35.189442999999997), (-106.58104, 35.189644000000001), (-106.58028, 35.193442999999995), (-106.580029, 35.194541000000001), (-106.57974399999999, 35.195785999999998), (-106.579475, 35.196961999999999), (-106.57922699999999, 35.198042999999998), (-106.578397, 35.201665999999996), (-106.57827999999999, 35.201642999999997), (-106.57737999999999, 35.201642999999997), (-106.57697999999999, 35.201543000000001), (-106.56436599999999, 35.200311999999997), (-106.56058, 35.199942999999998), (-106.56048, 35.197342999999996), (-106.56048, 35.195842999999996), (-106.56048, 35.194342999999996), (-106.56048, 35.193142999999999), (-106.56048, 35.191873999999999), (-106.56048, 35.191742999999995), (-106.56048, 35.190242999999995), (-106.56037999999999, 35.188642999999999), (-106.56037999999999, 35.187242999999995), (-106.56037999999999, 35.186842999999996), (-106.56037999999999, 35.186552999999996), (-106.56037999999999, 35.185842999999998), (-106.56037999999999, 35.184443000000002), (-106.56037999999999, 35.182943000000002), (-106.56037999999999, 35.181342999999998), (-106.56037999999999, 35.180433000000001), (-106.56037999999999, 35.179943000000002), (-106.56037999999999, 35.178542999999998), (-106.56037999999999, 35.177790999999999), (-106.56037999999999, 35.177143999999998), (-106.56037999999999, 35.175643999999998), (-106.56037999999999, 35.174444000000001), (-106.56037999999999, 35.174043999999995), (-106.560526, 35.174043999999995), (-106.56478, 35.174043999999995), (-106.56627999999999, 35.174143999999998), (-106.566541, 35.174144999999996), (-106.569023, 35.174157000000001), (-106.56917199999999, 35.174157999999998), (-106.56938, 35.174143999999998), (-106.57061499999999, 35.174143999999998), (-106.57097999999999, 35.174143999999998), (-106.57679999999999, 35.174143999999998), (-106.57798, 35.174143999999998)]

    test = [clockwise(v) for i in xrange(100)]
    print test.count(True)
    print test.count(False)
