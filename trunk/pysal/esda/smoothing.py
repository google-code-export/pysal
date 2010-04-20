"""
Apply smoothing to rate computation

[Longer Description]

Author(s):
    Myunghwa Hwang mhwang4@gmail.com
    Luc Anselin luc.anselin@asu.edu
    Serge Rey srey@asu.edu

"""
import pysal
from pysal.weights import comb
from pysal.cg import Point, Ray, LineSegment
from pysal.cg import get_angle_between, get_points_dist, get_segment_point_dist
from pysal.cg import get_point_at_angle_and_dist, convex_hull
from pysal.common import np
from pysal.weights.spatial_lag import lag as slag
from scipy.stats import gamma, chi2

def flatten(l,unique=True):
    """flatten a list of lists

    Parameters
    ----------
    l          : list of lists
    unique     : boolean
                 whether or not only unique items are wanted

    Returns
    -------
               : list of single items

    Examples
    --------
    >>> l = [[1,2],[3,4,],[5,6]]
    >>> flatten(l)
    [1, 2, 3, 4, 5, 6]
    """
    l = reduce(lambda x, y: x + y, l)
    if not unique: return list(l)
    return list(set(l))

def weighted_median(d, w):
    """A utility function to find a median of d based on w

    Parameters
    ----------
    d          : array (n, 1)
                 variable for which median will be found
    w          : array (n, 1)
                 variable on which d's medain will be decided

    Note
    ----
    d and w are arranged in the same order 

    Returns
    -------
               : numeric
                 median of d 
    
    Examples
    --------
    >>> d = np.array([5,4,3,1,2])
    >>> w = np.array([10,22,9,2,5])
    >>> weighted_median(d,w)
    4
    """
    dtype = [('w','%s' % w.dtype),('v','%s' % d.dtype)]
    d_w = np.array(zip(w,d),dtype=dtype)
    d_w.sort(order='v')
    reordered_w = d_w['w'].cumsum()
    cumsum_threshold = reordered_w[-1]*1.0/2
    median_inx = (reordered_w >= cumsum_threshold).nonzero()[0][0]
    if reordered_w[median_inx] == cumsum_threshold and len(d) - 1 > median_inx:
        return np.sort(d)[median_inx:median_inx + 2].mean()
    return np.sort(d)[median_inx]

def sum_by_n(d, w, n):
    """A utility function to summarize a data array into n values 
       after weighting the array with another weight array w
   
    Parameters
    ----------
    d          : array(t, 1)
                 numerical values
    w          : array(t, 1)
                 numerical values for weighting
    n          : integer
                 the number of groups 
                 t = c*n (c is a constant)

    Returns
    -------
               : array(n, 1)
                 an array with summarized values

    Examples
    --------
    >>> d = np.array([10, 9, 20, 30])
    >>> w = np.array([0.5, 0.1, 0.3, 0.8])
    >>> n = 2
    >>> sum_by_n(d, w, n)
    array([  5.9,  30. ])
    """
    t = len(d)
    h = t / n
    d = d * w
    return np.array([sum(d[i: i + h]) for i in range(0, t, h)])

def crude_age_standardization(e, b, n):
    """A utility function to compute rate through crude age standardization

    Parameters
    ----------
    e          : array(n*2*h, 1)
                 event variable measured for each gender/age group across n spatial units
    b          : array(n*2*h, 1)
                 population at risk variable measured for each gender/age group across n spatial units
    n          : integer
                 the number of spatial units 

    Note
    ----
    e and b are arranged in the same order

    Returns
    -------
               : array(n, 1)
                 age standardized rate

    Examples:
    >>> e = np.array([30, 25, 25, 15, 33, 21, 30, 20])
    >>> b = np.array([100, 100, 110, 90, 100, 90, 110, 90])
    >>> n = 2
    >>> crude_age_standardization(e, b, n)
    array([ 0.12025316,  0.13164557])
    """
    r = e * 1.0 / b
    age_weight = b * 1.0 / sum(b)
    return sum_by_n(r, age_weight, n)

def direct_age_standardization(e, b, s, n, alpha=0.05):
    """A utility function to compute rate through direct age standardization

    Parameters
    ----------
    e          : array(n*2*h, 1)
                 event variable measured for each gender/age group across n spatial units
    b          : array(n*2*h, 1)
                 population at risk variable measured for each gender/age group across n spatial units
    s          : array(n*2*h, 1)
                 standard million population for each gender/age group across n spatial units
    n          : integer
                 the number of spatial units 

    Note
    ----
    e, b, and s are arranged in the same order

    Returns
    -------
               : array(n, 1)
                 age standardized rate

    Examples:
    >>> e = np.array([30, 25, 25, 15, 33, 21, 30, 20])
    >>> b = np.array([1000, 1000, 1100, 900, 1000, 900, 1100, 900])
    >>> s = np.array([1000, 900, 1000, 900, 1000, 900, 1000, 900])
    >>> n = 2
    >>> [i[0] for i in direct_age_standardization(e, b, s, n)]
    [0.011872009569377989, 0.013325358851674639]
    """
    age_weight = (1.0 / b) * (s * 1.0 / sum(s))
    adjusted_r = sum_by_n(e, age_weight, n)
    var_estimate = sum_by_n(e, np.square(age_weight), n)
    g_a = np.square(adjusted_r) / var_estimate 
    g_b = var_estimate / adjusted_r
    k = [age_weight[i:i + len(b)/n].max() for i in range(0, len(b), len(b)/n)]
    g_a_k = np.square(adjusted_r + k)/(var_estimate + np.square(k))
    g_b_k = (var_estimate + np.square(k)) / (adjusted_r + k)
    summed_b = sum_by_n(b, np.ones(len(b)), n)
    res = []
    for i in range(len(adjusted_r)):
        if adjusted_r[i] == 0:
            upper = 0.5*chi2(1 - 0.5*alpha)
            lower = 0.0
        else:
            lower = gamma.ppf(0.5*alpha, g_a[i], scale=g_b[i])  
            upper = gamma.ppf(1 - 0.5 * alpha, g_a_k[i], scale=g_b_k[i]) 
        res.append((adjusted_r[i], lower, upper))
    return res

def indirect_age_standardization(b, r, n):
    """A utility function to compute rate through indirect age standardization

    Parameters
    ----------
    b          : array(n*2*h, 1)
                 population at risk variable measured for each gender/age group across n spatial units
    r          : array(n*2*h, 1)
                 reference rates for each gender/age group across n spatial units
    n          : integer
                 the number of spatial units 

    Note
    ----
    e and r are arranged in the same order

    Returns
    -------
               : array(n, 1)
                 age standardized rate

    Examples:
    >>> b = np.array([100, 100, 110, 90, 100, 90, 110, 90])
    >>> r = np.array([0.3, 0.2, 0.22, 0.31, 0.29, 0.15, 0.33, 0.2])
    >>> n = 2
    >>> indirect_age_standardization(b, r, n)
    array([ 0.12924051,  0.12253165])
    """
    age_weight = b * 1.0 / sum(b)
    return sum_by_n(r, age_weight, n)
    
class Excess_Risk:
    """Excess Risk

    Parameters
    ----------
    e		: array (n, 1)
    		  event variable measured across n spatial units
    b		: array (n, 1)
    		  population at risk variable measured across n spatial units

    Attributes
    ----------
    r		: array (n, 1)
		  execess risk values

    Examples
    --------
    >>> stl = pysal.open('../examples/stl_hom.csv', 'r')
    >>> stl_e, stl_b = np.array(stl[:,10]), np.array(stl[:,13])
    >>> er = Excess_Risk(stl_e, stl_b)
    >>> er.r[:10]
    array([ 0.20665681,  0.43613787,  0.42078261,  0.22066928,  0.57981596,
            0.35301709,  0.56407549,  0.17020994,  0.3052372 ,  0.25821905])
    >>>
    """
    def __init__(self, e, b):
        r_mean = e.sum() * 1.0 / b.sum()
	self.r = e * 1.0 / (b * r_mean)

class Empirical_Bayes: 
    """Aspatial Empirical Bayes Smoothing

    Parameters
    ----------
    e		: array (n, 1)
    		  event variable measured across n spatial units
    b		: array (n, 1)
    		  population at risk variable measured across n spatial units

    Attributes
    ----------
    r		: array (n, 1)
		  rate values from Empirical Bayes Smoothing

    Examples
    --------
    >>> stl = pysal.open('../examples/stl_hom.csv', 'r')
    >>> stl_e, stl_b = np.array(stl[:,10]), np.array(stl[:,13])
    >>> eb = Empirical_Bayes(stl_e, stl_b)
    >>> eb.r[:10]
    array([  2.36718950e-05,   4.54539167e-05,   4.78114019e-05,
             2.76907146e-05,   6.58989323e-05,   3.66494122e-05,
	     5.79952721e-05,   2.03064590e-05,   3.31152999e-05,
	     3.02748380e-05])
    >>>
    """
    def __init__(self, e, b):
	e_sum, b_sum = e.sum() * 1.0, b.sum() * 1.0
        r_mean = e_sum / b_sum
	rate = e * 1.0 / b
	r_variat = rate - r_mean
	r_var_left = (b * r_variat * r_variat).sum() * 1.0 / b_sum
	r_var_right = r_mean * 1.0 / b.mean() 
	r_var = r_var_left - r_var_right
	weight = r_var / ( r_var + r_mean / b)
	self.r = weight * rate + (1.0 - weight) * r_mean

class Spatial_Rate:
    """Spatial Rate Smoothing

    Parameters
    ----------
    e		: array (n, 1)
    		  event variable measured across n spatial units
    b		: array (n, 1)
    		  population at risk variable measured across n spatial units
    w		: spatial weights instance

    Attributes
    ----------
    r		: array (n, 1)
		  rate values from spatial rate smoothing

    Examples
    --------
    >>> stl = pysal.open('../examples/stl_hom.csv', 'r')
    >>> stl_e, stl_b = np.array(stl[:,10]), np.array(stl[:,13])
    >>> stl_w = pysal.open('../examples/stl.gal', 'r').read()
    >>> if not stl_w.id_order: stl_w.id_order = range(1,len(stl) + 1)
    >>> sr = Spatial_Rate(stl_e,stl_b,stl_w)
    >>> sr.r[:10]
    array([  4.59326407e-05,   3.62437513e-05,   4.98677081e-05,
             5.09387329e-05,   3.72735210e-05,   4.01073093e-05,
	     3.79372794e-05,   3.27019246e-05,   4.26204928e-05,
             3.47270722e-05])
    """
    def __init__(self, e, b, w):
	if not w.id_order_set:
            raise ValueError("w id_order must be set to align with the order of e and b")
        else:
	    w.transform = 'b'
            w_e, w_b = slag(w, e), slag(w, b)
	    self.r = (e + w_e) / (b + w_b)

class Disk_Smoother:
    """Locally weighted averages or disk smoothing

    Parameters
    ----------
    e           : array (n, 1)
                  event variable measured across n spatial units
    b           : array (n, 1)
                  population at risk variable measured across n spatial units
    w           : spatial weights matrix

    Attributes
    ----------
    r           : array (n, 1)
                  rate values from disk smoothing

    Examples
    --------
    >>> stl = pysal.open('../examples/stl_hom.csv', 'r')
    >>> stl_e, stl_b = np.array(stl[:,10]), np.array(stl[:,13])
    >>> stl_w = pysal.open('../examples/stl.gal', 'r').read()
    >>> if not stl_w.id_order: stl_w.id_order = range(1,len(stl) + 1)
    >>> sr = Disk_Smoother(stl_e,stl_b,stl_w)
    >>> sr.r[:10]
    array([  4.56502262e-05,   3.44027685e-05,   3.38280487e-05,
             4.78530468e-05,   3.12278573e-05,   2.22596997e-05,
             2.67074856e-05,   2.36924573e-05,   3.48801587e-05,
             3.09511832e-05])
    """

    def __init__(self, e, b, w):
        if not w.id_order_set:
            raise ValueError("w id_order must be set to align with the order of e and b")
        else:
            r = e * 1.0 / b
            weight_sum = []
            for i in w.id_order:
                weight_sum.append(sum(w.weights[i]))
            self.r = slag(w, r) / np.array(weight_sum)

class Spatial_Median_Rate:
    """Spatial Median Rate Smoothing

    Parameters
    ----------
    e		: array (n, 1)
    		  event variable measured across n spatial units
    b		: array (n, 1)
    		  population at risk variable measured across n spatial units
    w		: spatial weights instance
    aw		: array (n, 1) 
    		  auxiliary weight variable measured across n spatial units
    iteration	: integer 
    		  the number of interations

    Attributes
    ----------
    r		: array (n, 1)
		  rate values from spatial median rate smoothing
    w           : spatial weights instance
    aw          : array (n, 1) 
	          auxiliary weight variable measured across n spatial units

    Examples
    --------
    >>> stl = pysal.open('../examples/stl_hom.csv', 'r')
    >>> stl_e, stl_b = np.array(stl[:,10]), np.array(stl[:,13])
    >>> stl_w = pysal.open('../examples/stl.gal', 'r').read()
    >>> if not stl_w.id_order: stl_w.id_order = range(1,len(stl) + 1)
    >>> smr0 = Spatial_Median_Rate(stl_e,stl_b,stl_w)
    >>> smr0.r[:10]
    array([  3.96047383e-05,   3.55386859e-05,   3.28308921e-05,
             4.30731238e-05,   3.12453969e-05,   1.97300409e-05,
             3.10159267e-05,   2.19279204e-05,   2.93763432e-05,
             2.93763432e-05])
    >>> smr1 = Spatial_Median_Rate(stl_e,stl_b,stl_w,iteration=5)
    >>> smr1.r[:10]
    array([  3.11293620e-05,   2.95956330e-05,   3.11293620e-05,
             3.10159267e-05,   2.98436066e-05,   2.76406686e-05,
             3.10159267e-05,   2.94788171e-05,   2.99460806e-05,
             2.96981070e-05])
    >>> smr2 = Spatial_Median_Rate(stl_e,stl_b,stl_w,aw=stl_b)
    >>> smr2.r[:10]
    array([  5.77412020e-05,   4.46449551e-05,   5.77412020e-05,
             5.77412020e-05,   4.46449551e-05,   3.61363528e-05,
             3.61363528e-05,   4.46449551e-05,   5.77412020e-05,
             4.03987355e-05])
    >>> smr3 = Spatial_Median_Rate(stl_e,stl_b,stl_w,aw=stl_b,iteration=5)
    >>> smr3.r[:10]
    array([  3.61363528e-05,   4.46449551e-05,   3.61363528e-05,
             3.61363528e-05,   4.46449551e-05,   3.61363528e-05,
             3.61363528e-05,   4.46449551e-05,   3.61363528e-05,
             4.46449551e-05])
    >>>
    """
    def __init__(self, e, b, w, aw=None, iteration=1):
	if not w.id_order_set:
            raise ValueError("w id_order must be set to align with the order of e and b")
	self.r = e * 1.0 / b
	self.aw, self.w = aw, w
	while iteration:
	    self.__search_median()
	    iteration -= 1
    
    def __search_median(self):
	r, aw, w = self.r, self.aw, self.w
        new_r = [] 
	if self.aw == None:
	    for i, id in enumerate(w.id_order):
		r_disk = np.append(r[i], r[w.neighbor_offsets[id]])
                new_r.append(np.median(r_disk))
    	else:
	    for i, id in enumerate(w.id_order):
	        id_d = [i] + list(w.neighbor_offsets[id])
                aw_d, r_d = aw[id_d], r[id_d]
                new_r.append(weighted_median(r_d,aw_d))
	self.r = np.array(new_r)

class Headbanging_Triples:
    """Generate a pseudo spatial weights instance that contains headbaning triples

    Parameters
    ----------
    data	: array (n, 2)
    		  numpy array of x, y coordinates
    w		: spatial weights instance
    k       : integer number of nearest neighbors
    t		: integer
    		  the number of triples
    angle	: integer between 0 and 180
    		  the angle criterium for a set of triples
    edgecorr	: boolean 
    		  whether or not correction for edge points is made
    
    Attributes
    ----------
    triples	: dictionary
    		  key is observation record id, value is a list of lists of triple ids
    extra       : dictionary
                  key is observation record id, value is a list of the following:
                  tuple of original triple observations 
                  distance between original triple observations
                  distance between an original triple observation and its extrapolated point

    Examples
    --------
    >>> from pysal import knnW
    >>> stl_db = pysal.open('../examples/stl_hom.csv','r')
    >>> fromWKT = pysal.core._FileIO.wkt.WKTParser()
    >>> stl_db.cast('WKT',fromWKT)
    >>> d = np.array([i.centroid for i in stl_db[:,0]])
    >>> w = knnW(d,k=5)
    >>> if not w.id_order_set: w.id_order = w.id_order
    >>> ht = Headbanging_Triples(d,w,k=5)
    >>> for k, item in ht.triples.items()[:5]: print k, item
    0 [(5, 6), (10, 6)]
    1 [(4, 7), (4, 14), (9, 7)]
    2 [(0, 8), (10, 3), (0, 6)]
    3 [(4, 2), (2, 12), (8, 4)]
    4 [(8, 1), (12, 1), (8, 9)]
    >>> sids = pysal.open('../examples/sids2.shp','r')
    >>> sids_d = np.array([i.centroid for i in sids])
    >>> sids_w = knnW(sids_d,k=5)
    >>> if not sids_w.id_order_set: sids_w.id_order = sids_w.id_order
    >>> s_ht = Headbanging_Triples(sids_d,sids_w,k=5)
    >>> for k, item in s_ht.triples.items()[:5]: print k, item
    0 [(1, 18), (1, 21), (1, 33)]
    1 [(2, 40), (2, 22), (22, 40)]
    2 [(39, 22), (1, 9), (39, 17)]
    3 [(16, 6), (19, 6), (20, 6)]
    4 [(5, 15), (27, 15), (35, 15)]
    >>> s_ht2 = Headbanging_Triples(sids_d,sids_w,k=5,edgecor=True)
    >>> for k, item in s_ht2.triples.items()[:5]: print k, item
    0 [(1, 18), (1, 21), (1, 33)]
    1 [(2, 40), (2, 22), (22, 40)]
    2 [(39, 22), (1, 9), (39, 17)]
    3 [(16, 6), (19, 6), (20, 6)]
    4 [(5, 15), (27, 15), (35, 15)]
    >>> extrapolated = s_ht2.extra[72]
    >>> extrapolated[0]
    (89, 77)
    >>> round(extrapolated[1],5), round(extrapolated[2],6)
    (0.33753, 0.302707)
    """
    def __init__(self, data, w, k=5, t=3, angle=135.0, edgecor=False):
        if k < 3:
	         raise ValueError("w should be NeareastNeighbors instance & the number of neighbors should be more than 3.")
        if not w.id_order_set:
            raise ValueError("w id_order must be set to align with the order of data")
        self.triples, points = {}, {}
        for i, pnt in enumerate(data):
            ng = w.neighbor_offsets[i]
            points[(i,Point(pnt))] = dict(zip(ng,[Point(d) for d in data[ng]]))
        for i, pnt in points.keys():
            ng = points[(i,pnt)]
            tr, tr_dis = {}, []
            for c in comb(ng.keys(), 2):
                p2, p3 = ng[c[0]], ng[c[-1]]
                ang = get_angle_between(Ray(pnt,p2),Ray(pnt,p3))
                if ang > angle or (ang < 0.0 and ang + 360 > angle):
                    tr[tuple(c)] = (p2, p3)
            if len(tr) > t:
		for c in tr.keys():
                    p2, p3 = tr[c]
                    tr_dis.append((get_segment_point_dist(LineSegment(p2,p3), pnt),c))
                tr_dis = sorted(tr_dis)[:t]
                self.triples[i] = [trp for dis, trp in tr_dis]
            else:
                self.triples[i] = tr.keys()
        if edgecor:
            self.extra = {}
            ps = dict([(p, i) for i, p in points.keys()])
            chull = convex_hull(ps.keys())
            chull = [p for p in chull if len(self.triples[ps[p]]) == 0]
            for point in chull:
                key = (ps[point], point)
                ng = points[key]
                ng_dist = [(get_points_dist(point, p),p) for p in ng.values()]
                ng_dist_s = sorted(ng_dist,reverse=True)
                extra = None
                while extra is None and len(ng_dist_s) > 0:
                    p2 = ng_dist_s.pop()[-1]
                    p3s = ng.values()
                    p3s.remove(p2)
                    for p3 in p3s:
                        dist_p2_p3 = get_points_dist(p2, p3)
                        dist_p_p2 = get_points_dist(point, p2)
                        dist_p_p3 = get_points_dist(point, p3)
                        if dist_p_p2 <= dist_p_p3:
                            ray1,ray2,s_pnt,dist,c = Ray(p2, point),Ray(p2, p3),p2,dist_p_p2,(ps[p2],ps[p3])
                        else:
                            ray1,ray2,s_pnt,dist,c = Ray(p3, point),Ray(p3, p2),p3,dist_p_p3,(ps[p3],ps[p2])
                        ang = get_angle_between(ray1,ray2)
                        if ang >= 90 + angle/2 or (ang < 0 and ang + 360 >= 90 + angle/2):
                            ex_point = get_point_at_angle_and_dist(ray1, angle, dist)
                            extra = [c, dist_p2_p3, get_points_dist(s_pnt, ex_point)]
                            break
                self.triples[ps[point]].append(extra[0])
                self.extra[ps[point]] = extra
        
class Headbanging_Median_Rate:
    """Headbaning Median Rate Smoothing

    Parameters
    ----------
    e		: array (n, 1)
    		  event variable measured across n spatial units
    b		: array (n, 1)
    		  population at risk variable measured across n spatial units
    t		: Headbanging_Triples instance
    aw		: array (n, 1)
    		  auxilliary weight variable measured across n spatial units
    iteration 	: integer
    		  the number of iterations

    Attributes
    ----------
    r		: array (n, 1)
    		  rate values from headbaning median smoothing
   
    Examples
    --------
    >>> from pysal import knnW
    >>> sids = pysal.open('../examples/sids2.shp', 'r')
    >>> sids_d = np.array([i.centroid for i in sids])
    >>> sids_w = knnW(sids_d,k=5)
    >>> if not sids_w.id_order_set: sids_w.id_order = sids_w.id_order
    >>> s_ht = Headbanging_Triples(sids_d,sids_w,k=5)
    >>> sids_db = pysal.open('../examples/sids2.dbf', 'r')
    >>> s_e, s_b = np.array(sids_db[:,9]), np.array(sids_db[:,8])
    >>> sids_hb_r = Headbanging_Median_Rate(s_e,s_b,s_ht)
    >>> sids_hb_r.r[:5]
    array([ 0.00075586,  0.        ,  0.0008285 ,  0.0018315 ,  0.00498891])
    >>> sids_hb_r2 = Headbanging_Median_Rate(s_e,s_b,s_ht,iteration=5)
    >>> sids_hb_r2.r[:5]
    array([ 0.0008285 ,  0.00084331,  0.00086896,  0.0018315 ,  0.00498891])
    >>> sids_hb_r3 = Headbanging_Median_Rate(s_e,s_b,s_ht,aw=s_b)
    >>> sids_hb_r3.r[:5]
    array([ 0.00091659,  0.        ,  0.00156838,  0.0018315 ,  0.00498891])
    """
    def __init__(self, e, b, t, aw=None, iteration=1):
        self.r = e * 1.0 / b
        self.tr, self.aw = t.triples, aw
        if hasattr(t, 'exta'): self.extra = t.extra
        while iteration:
            self.__search_headbanging_median()
            iteration -= 1

    def __get_screens(self, id, triples, weighted=False):
        r, tr = self.r, self.tr
        if len(triples) == 0: return r[id]
        if hasattr(self, 'extra') and self.extra.has_key(id):
            extra = self.extra
            trp_r = r[list(triples[0])]
            trp_r[-1] = trp_r[0] + (trp_r[0] - trp_r[-1])*(extra[id][-1]*1.0/extra[id][1])
            trp_r = sorted(trp_r)
            if not weighted: return r, trp_r[0], trp_r[-1]
            else:
                trp_aw = self.aw[trp]
            	extra_w = trp_aw[0] + (trp_aw[0] - trp_aw[-1])*(extra[id][-1]*1.0/extra[id][1])
                return r, trp_r[0], trp_r[-1], self.aw[id], trp_aw[0] + extra_w
        if not weighted:
            lowest, highest = [], []
            for trp in triples:
                trp_r = np.sort(r[list(trp)])
                lowest.append(trp_r[0])
                highest.append(trp_r[-1])
            return r[id], np.median(np.array(lowest)), np.median(np.array(highest))
        if weighted:
            lowest, highest = [], []
            lowest_aw, highest_aw = [], []
            for trp in triples:
                trp_r = r[list(trp)]
                dtype = [('r','%s' % trp_r.dtype), ('w','%s' % self.aw.dtype)]
                trp_r = np.array(zip(trp_r,list(trp)),dtype=dtype)
                trp_r.sort(order='r')
                lowest.append(trp_r['r'][0])
                highest.append(trp_r['r'][-1])
                lowest_aw.append(self.aw[trp_r['w'][0]])
                highest_aw.append(self.aw[trp_r['w'][-1]])
            wm_lowest = weighted_median(np.array(lowest),np.array(lowest_aw))
            wm_highest = weighted_median(np.array(highest),np.array(highest_aw))
            triple_members = flatten(triples,unique=False)
            return r[id], wm_lowest, wm_highest, self.aw[id]*len(triples), self.aw[triple_members].sum()

    def __get_median_from_screens(self, screens):
        if isinstance(screens, float): return screens
        elif len(screens) == 3: return np.median(np.array(screens))
        elif len(screens) == 5: 
            rk, wm_lowest, wm_highest, w1, w2 = screens
            if rk >= wm_lowest and rk <= wm_highest: return rk
            elif rk < wm_lowest and w1 < w2: return wm_lowest
            elif rk > wm_highest and w1 < w2: return wm_highest
            else: return rk
     
    def __search_headbanging_median(self):
        r, tr = self.r, self.tr
        new_r = []
        for k in tr.keys():
            screens = self.__get_screens(k, tr[k], weighted=(self.aw!=None))
            new_r.append(self.__get_median_from_screens(screens))
        self.r = np.array(new_r)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
