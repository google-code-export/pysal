

import numpy as np
import matplotlib.pyplot as plt

s = np.loadtxt("seq_results.txt")
p = np.loadtxt("pp_results.txt")
c = np.loadtxt("cl_results.txt")
m = np.loadtxt("mp_results.txt")


sp = s[0:-1]/p[0:-1]
sc = s[0:-1]/c[0:-1]
sm = s[0:-1]/m[0:-1]

ns = [ 125, 250, 500, 1000, 2000, 4000, 8000]
leg = ["PyOpenCL","Multiprocessing", "PP"]
#plt.plot(ns, sequential)
plt.plot(ns, sc[:,0], ns, sm[:,0], ns, sp[:,0],)
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=5")
plt.show()
plt.plot(ns, sc[:,1], ns, sm[:,1], ns, sp[:,1],)
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=7")
plt.show()

plt.plot(ns, sc[:,2], ns, sm[:,2], ns, sp[:,2],)
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=9")
plt.show()


sp = s/p
sm = s/m

leg = ["Multiprocessing", "PP"]
ns = [ 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
plt.plot(ns, sm[:,2], ns, sp[:,2],)
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=9")
plt.show()



