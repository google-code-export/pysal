from mapclassify_V2 import Fisher_Jenks_1, PFisher_Jenks, PFisher_Jenks_MP, PFisher_Jenks_PP
import numpy as np
import time 

np.random.seed(100)

ns = [125,250,500,1000,2000,4000,8000,16000]
ks = [5,7,9]
results = np.zeros((len(ns),len(ks)))

datall = np.random.rand(max(ns))
for i,n in enumerate(ns):
    dat = datall[0:n]
    for j,k in enumerate(ks):
        print n,k
        try:
            t1 = time.time()
            o4 = Fisher_Jenks_1(dat)
            t2 = time.time()
            results[i, j] = t2 - t1
        except:
            pass
        print 'FJ: ',results[i, j]

np.savetxt('seq_results.txt',results)
