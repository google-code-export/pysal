

import numpy as np
import matplotlib.pyplot as plt

t = np.loadtxt("pp_results.txt")
s = np.loadtxt("seq_results.txt")

sp = s/t
t=sp

ns = [ 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
leg = ["k=5","k=7", "k=9"]
#plt.plot(ns, sequential)
plt.plot(ns, t[:,0], 'g-.',  ns, t[:,1], 'r:', ns, t[:,2], 'b-' )
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("Parallel Python Speedup")



plt.show()
