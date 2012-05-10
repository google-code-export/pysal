"""
Generation of test data with known structure for FJ classification
"""
import numpy as np

def gen_structure_data(n,k):
    w = n/k
    r = n%k
    ws = [w] * k
    ws[-1] = ws[-1]+r
    x = np.zeros((n,))
    ends = np.cumsum(ws).tolist()
    start = [0]
    start.extend(ends[0:-1])
    ij = zip(start,ends)
    c=1
    for i,j in ij:
        x[i:j] = c
        c += 1
    return x


if __name__ == '__main__':
    #from mapclassify_V2 import *
    from pysal import Fisher_Jenks

    n = 1000
    k = 7

    x1000_7 = gen_structure_data(n,k)

    fj_1000_7 = Fisher_Jenks(x1000_7, k=7)
