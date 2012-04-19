import numpy as np
import matplotlib.pyplot as plt

d1 = np.loadtxt("results.txt")
d2 = np.loadtxt("results2.txt")
d = np.vstack((d1,d2))
d.shape = (6,4,7)

sequential = d[:,0,:]
cl = d[:,1,:]
mp = d[:,2,:]
pp = d[:,3,:]

scl = sequential/cl
smp = sequential/mp
spp = sequential/pp

ns = [ 125, 250, 500, 1000, 2000, 4000]
#plt.plot(ns, sequential)
leg = ["cl", "mp", "pp"]
plt.plot(ns, scl[:,0], ns, smp[:,0], ns,spp[:,0] )
plt.legend(leg, loc='lower right')
plt.title("Speedup k = 4")
plt.xlabel("n")
plt.ylabel("Ts/Tp")



plt.show()
