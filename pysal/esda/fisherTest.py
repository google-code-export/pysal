from mapclassify_V2 import Fisher_Jenks_1, PFisher_Jenks, PFisher_Jenks_MP, PFisher_Jenks_PP
import numpy as np
import time 

np.random.seed(100)

ns = [100, 500, 1000, 2000]
ks = [4,5,6]

results = {}
for k in ks:
    res = np.zeros((4,4))
    for i,n in enumerate(ns):
        print n,k
        dat = np.random.rand(n)
        t1 = time.time()
        o1 = Fisher_Jenks_1(dat)
        t2 = time.time()
        res[0, i] = t2-t1
        print 'FJ: ',res[0, i]
        o2 = PFisher_Jenks(dat)
        t3 = time.time()
        res[1, i] = t3-t2
        print 'FJCL: ',res[1, i]
        o3 = PFisher_Jenks_MP(dat)
        t4 = time.time()
        res[2, i] = t4-t3
        print 'FJMP: ',res[2, i]
        o4 = PFisher_Jenks_PP(dat)
        t5 = time.time()
        res[3, i] = t5-t4
        print 'FJPP: ',res[3, i]
    results[k] = res
