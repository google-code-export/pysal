"""
Winged-edge Data Structure for Networks

"""

__author__ = "Sergio J. Rey <srey@asu.edu>"

import pysal as ps
import numpy as np






def regions_from_graph(vertices, edges):
    """
    Extract regions from vertices and edges of a planar graph

    Arguments
    ---------

    vertices: dictionary with vertex id as key, coordinates of vertex as value

    edges: list of (head,tail) edges

    Returns
    ------

    regions: list of lists of nodes defining a region. Includes the external
    region



    Examples
    --------
    >>> vertices = {1: (1,2), 2:(0,1), 3:(2,1), 4:(0,0), 5:(2,0)}
    >>> edges = [ (1,2), (1,3), (2,3), (2,4), (4,5), (5,3) ]
    >>> r = regions_from_graph(vertices, edges)
    >>> r
    [[1, 2, 3, 1], [1, 3, 5, 4, 2, 1], [2, 4, 5, 3, 2]]


    Notes
    -----

    Based on Jiang, X.Y. and H. Bunke (1993) "An optimal algorithm for
    extracting the regions of a plane graph." Pattern Recognition Letters,
    14:533-558.
    """

    # step 1
    # have a twin for each directed edge
    dedges = edges[:]
    for edge in edges:
        new_edge = edge[1], edge[0]
        if new_edge not in dedges:
            dedges.append( (edge[1],edge[0]) )

    # step 2 complement each directed edge with an angle formed with horizontal
    # line passing through edge[0] for each edge
    angles = []
    from math import atan2, degrees

    for edge in dedges:

        v1 = vertices[edge[0]]
        v2 = vertices[edge[1]]
        dx = v2[0] - v1[0]
        dy = v2[1] - v1[1]
        at = atan2(dy, dx)
        d = degrees(at)
        if d < 0:
            d = 360 + d
        angles.append( [ (edge[0],d), (edge[0],edge[1]) ])

    # step 3 sort the list into ascending order using vi and angle as primary and
    # secondary keys
    angles.sort()


    # form wedges on consecutive entries with same vi (vi,vj,dij), (vi,vk,dik)
    # gives the wedge (vk,vi,vj)
    wedges = []
    start = angles[0]
    c = 0
    for i in range(1,len(angles)):
        next_edge = angles[i]
        previous_edge = angles[i-1]
        if next_edge[0][0] == start[0][0]:
            wedge = [ next_edge[1][1], previous_edge[1][0], previous_edge[1][1] ]
            wedges.append(wedge)
        else:
            # first form wedge with last and first entry of current group
            # to do
            wedge = [ start[1][1], previous_edge[1][0], previous_edge[1][1] ]
            wedges.append(wedge)
            start = next_edge

    # final pair

    wedge = [ start[1][1], previous_edge[1][0], next_edge[1][1] ]
    wedges.append(wedge)


    # phase two
    # form regions from contiguous wedges

    nw = len(wedges)
    used = [0]*nw
    wedges.sort()
    #print wedges

    #print 'forming regions'

    i = 0
    regions = []
    while sum(used) < nw:
        i = used.index(0)
        wi = wedges[i]
        start = wedges[i]
        used[i] = 1
        region = [start]
        # find next contiguous wedge for wi
        forming = True
        while forming:


            # find first wedge contiguous to wi
            for j in xrange(nw):
                wj = wedges[j]
                if wj[0] ==  wi[1] and wj[1] == wi[2]:
                    region.append(wj)
                    used[j] = 1
                    wi = wj
                    if wi[1] == start[0] and wi[2] == start[1]:
                        forming = False
                        regions.append(region)
                        #print start, regions
                        #raw_input('h')
                    break

    # put in closed cartographic form
    nodes = []
    for region in regions:
        wedge0 = [ wedge[0] for wedge in region]
        wedge0.append(wedge0[0])
        nodes.append(wedge0)

    return nodes


def pcw(coords):
    """ test if polygon coordinates are clockwise ordered """
    n = len(coords)
    xl = coords[0:n-1,0]
    yl = coords[1:,1]
    xr = coords[1:,0]
    yr = coords[0:n-1,1]
    a = xl*yl - xr*yr
    area = a.sum()
    if area < 0:
        return 1
    else:
        return 0
     
class WED(object):
    """
    Winged-Edge data structure for a planar network.

    Arguments
    ---------

    vertices: dictionary with ids as key and value a tuple of coordinates for the vertex

    edges: list of edge tuples (o,d) where o is origin vertex, d is destination vertex

    Notes
    -----

    This implementation follows the description in Okabe and Sugihara (2012)
    "Spatial Analysis Along Networks: Statistical and Computational Methods."
    Wiley. Details are from Section 3.1.2.

    As the start_c, end_c, start_cc, and end_cc pointers are only vaguely
    described, the logic from
    http://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/model/winged-e.html is
    used to implement these points


    Examples
    -------

    >>> network = _lat2Network(3)
    >>> vertices = network['nodes']
    >>> edges = network['edges'] 
    >>> we1 = WED(vertices, edges)
    >>> we1.regions
    {0: [0, 1, 2, 3, 7, 11, 15, 14, 13, 12, 8, 4, 0], 1: [0, 4, 5, 1, 0], 2: [1, 5, 6, 2, 1], 3: [2, 6, 7, 3, 2], 4: [4, 8, 9, 5, 4], 5: [5, 9, 10, 6, 5], 6: [6, 10, 11, 7, 6], 7: [8, 12, 13, 9, 8], 8: [9, 13, 14, 10, 9], 9: [10, 14, 15, 11, 10]}
    >>> we1.cw_face_edges(5)
    [(9, 5), (5, 6), (6, 10), (10, 9)]
    """
 
    def __init__(self, vertices, edges):
        super(WED, self).__init__()
        regions = regions_from_graph(vertices,edges)
        regions = dict( [ (i,c) for i,c in enumerate(regions)])
        self.regions = regions
        self.node_link = {}     # key: node, value: incident link (edge)
        self.region_link = {}   # key: region (face), value: incident link (edge) 
        self.start_node = {}    # key: link (edge), value: start node 
        self.end_node = {}      # key: link (edge), value: end node 
        self.right_region = {}  # key: link (edge), value: region (face)
        self.left_region = {}   # key: link (edge), value: region (face)
        self.pred_left = {}     # key: link (edge), predecessor edge to edge
                                # when traversing left region cw
        self.succ_left = {}     # key: link (edge), successor edge to edge
                                # when traversing left region cw
        self.pred_right = {}    # key: link (edge), predecessor edge to edge
                                # when traversing right region cw
        self.succ_right = {}    # key: link (edge), successor edge to edge
                                # when traversing right region cw

        for r,region in enumerate(regions):
            nodes = regions[region]
            self.region_link[region] = (nodes[0],nodes[1])
            cw = pcw(np.array([vertices[i] for i in nodes]))
            if cw:

                # this is the external region
                self.external_region = r
                for j in xrange(len(nodes)-1):
                    start_node = nodes[j]
                    end_node = nodes[j+1]
                    self.start_node[(start_node, end_node)] = start_node
                    self.end_node[(start_node, end_node)] = end_node
                    self.left_region[(start_node, end_node)] = r
                    self.right_region[(end_node, start_node)] = r
            else:
                for j in xrange(len(nodes)-1):
                    start_node = nodes[j]
                    end_node = nodes[j+1]
                    self.start_node[(start_node, end_node)] = start_node
                    self.end_node[(start_node, end_node)] = end_node
                    self.left_region[(start_node, end_node)] = r
                    self.right_region[(end_node, start_node)] = r


        # left and right traverse
        for edge in self.left_region:
            left_r = self.left_region[edge]
            right_r = self.right_region[edge]

            if left_r == self.external_region:
                # coords are clockwise

                lnodes = self.regions[left_r]
                s = lnodes.index(edge[0])
                e = lnodes.index(edge[1])

                pred_left = (lnodes[e+1], lnodes[e])
                if s==0:
                    succ_left = (lnodes[-1], lnodes[-2])
                else:
                    succ_left = (lnodes[s], lnodes[s-1])


                rnodes = self.regions[right_r]
                s = rnodes.index(edge[0])
                e = rnodes.index(edge[1])
                pred_right = (rnodes[s+1], rnodes[s])
                if e==0:
                    succ_right = (rnodes[-1], rnodes[-2])
                else:
                    succ_right = (rnodes[e], rnodes[e-1])


                self.pred_left[edge] = pred_left
                self.succ_left[edge] = succ_left
                self.pred_right[edge] = pred_right
                self.succ_right[edge] = succ_right
                
            else:
                # coords are ccw
                lnodes = self.regions[left_r]
                s = lnodes.index(edge[0])
                e = lnodes.index(edge[1])
                if s == 0:
                    pred_left = (lnodes[e+1], lnodes[e])
                    succ_left = (lnodes[-1], lnodes[-2])
                else:
                    pred_left = (lnodes[e+1], lnodes[e])
                    succ_left = (lnodes[s], lnodes[s-1])

                rnodes = self.regions[right_r]
                s = rnodes.index(edge[0])
                e = rnodes.index(edge[1])
                if s == 0:
                    pred_right = (rnodes[1], rnodes[0])
                    succ_right = (rnodes[-2], rnodes[-3])
                else:
                    pred_right = (rnodes[s+1], rnodes[s])
                    if e==0:
                        succ_right = (rnodes[-1 ], rnodes[-2 ])
                    else:
                        succ_right = (rnodes[e], rnodes[e-1])

                self.pred_left[edge] = pred_left
                self.succ_left[edge] = succ_left
                self.pred_right[edge] = pred_right
                self.succ_right[edge] = succ_right


    def cw_face_edges(self,face):
        """
        Return the edges defining a face in cw order
        """

        l0 = self.region_link[face]
        if face == self.left_region[l0]:
            l0 = (l0[1], l0[0])
        l = l0

        traversing = True
        edges = []
        while traversing:
            edges.append(l)
            r = self.right_region[l]
            if r == face:
                l = self.succ_right[l]
            else:
                l = self.succ_left[l]
            if l == l0:
                traversing = False
        return edges

        
def incident_cw_edges_node(node):
    """Clockwise traversal of edges incident with node

    Arguments
    ---------

    node: Vertex instance

    Returns
    ------
    edges: list of edges that are cw incident with node

    """
    l0 = node.edge
    l = l0
    edges = []
    traversing = True
    while traversing:
        edges.append(l)
        v = l.start
        if v == node:
            l = l.pr
        else:
            l = l.pl
        #print l0, l
        if l0 == l:
            traversing = False
        #raw_input('here')
    return edges


def _lat2Network(k):
    """helper function to create a network from a square lattice.
    
    Used for testing purposes 
    """
    lat = ps.lat2W(k+1,k+1) 
    k1 = k+1
    nodes = {}
    edges = []
    for node in lat.id_order:
        for neighbor in lat[node]:
            edges.append((node,neighbor))
        nodes[node] = ( node/k1, node%k1 )

    res = {"nodes": nodes, "edges": edges}

    return res

class NPWED(object):
    """Winged edge data structure for Nonplanar network"""
    def __init__(self, G, P):
        super(NPWED, self).__init__()
        self.G = G
        self.P = P
        self.node_link = {}     # key: node, value: incident link (edge)
        self.start_node = {}    # key: link (edge), value: start node 
        self.end_node = {}      # key: link (edge), value: end node 
        self.start_c_link = {}  # key: link, value: first incident cw link 
        self.start_cc_link = {} # key: link, value: first incident ccw link 
        self.end_c_link = {}    # key: link, value: first incident cw link (end node)
        self.end_cc_link = {}   # key: link, value: first incident ccw link (end node)

        for edge in self.G.edges():
            s,e = edge
            self.node_link[s] = edge
            self.start_node[edge] = s
            self.end_node[edge] = e

    def incident_links(self, node):
        links = []
        links.extend(self.G.out_edges(node))
        links.extend(self.G.in_edges(node))
        return links







        
        
if __name__ == '__main__':


    # test region extraction

    vertices = {1: (1,2),
            2:(0,1),
            3:(2,1),
            4:(0,0),
            5:(2,0)}

    edges = [
            (1,2),
            (1,3),
            (2,3),
            (2,4),
            (4,5),
            (5,3) ]

    #r = regions_from_graph(vertices,edges)
    #we0 = WED(vertices,edges)


    network = _lat2Network(3)
    vertices = network['nodes']
    edges = network['edges']
    r1 = regions_from_graph(vertices, edges)
    we1 = WED(vertices,edges)



