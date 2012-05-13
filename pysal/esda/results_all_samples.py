

import numpy as np
import matplotlib.pyplot as plt

s = np.loadtxt("seq_results.txt")
p = np.loadtxt("pp_results.txt")
c = np.loadtxt("cl_results.txt")
m = np.loadtxt("mp_results.txt")



sp = s/p
sc = s/c
sm = s/m
ns = [ 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
leg = ["PyOpenCL (CPU) ","Multiprocessing", "PP"]
plt.plot(ns, sc[:,0], 'g-', ns, sm[:,0], 'b--', ns, sp[:,0], 'r-.')
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=5")
plt.show()
plt.plot(ns, sc[:,1], 'g-',  ns, sm[:,1], 'b--',  ns, sp[:,1], 'r-.')
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=7")
plt.show()

plt.plot(ns, sc[:,2], 'g-',  ns, sm[:,2], 'b--',  ns, sp[:,2], 'r-.')
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Comparative Speedups k=9")
plt.show()

