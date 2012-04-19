from mapclassify_V2 import Fisher_Jenks_1, PFisher_Jenks, PFisher_Jenks_MP, PFisher_Jenks_PP
import numpy as np
import time 

np.random.seed(100)

ns = [125, 250, 500, 1000, 2000, 4000, 8000]
ks = [5,7,9]
results = np.zeros((len(ns),4,len(ks)))

for i,n in enumerate(ns):
    for j,k in enumerate(ks):
        print n,k
        dat = np.random.rand(n)
        t1 = time.time()
        o1 = Fisher_Jenks_1(dat)
        t2 = time.time()
        results[i, 0, j] = t2-t1
        print 'FJ: ',results[i, 0, j]
        o2 = PFisher_Jenks(dat)
        t3 = time.time()
        results[i, 1, j] = t3-t2
        print 'FJCL: ',results[i,1, j]
        o3 = PFisher_Jenks_MP(dat)
        t4 = time.time()
        results[i, 2, j] = t4-t3
        print 'FJMP: ',results[i,2, j]
        o4 = PFisher_Jenks_PP(dat)
        t5 = time.time()
        results[i, 3, j] = t5-t4
        print 'FJPP: ',results[i,3, j]

with file('results.txt', 'w') as outfile:
    outfile.write('# Array shape: {0}\n'.format(results.shape))

    for n, data_slice in enumerate(results):
        outfile.write('# n=%f\n'%ns[n])
        np.savetxt(outfile, data_slice, fmt="%-8.3f")
