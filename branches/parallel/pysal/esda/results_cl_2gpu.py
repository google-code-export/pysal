
import numpy as np
import matplotlib.pyplot as plt

t = np.loadtxt("cl_results_2GPU_munny.txt")
s = np.loadtxt("seq_results.txt")

sp = s[0:-1]/t[0:-1]

ns = [ 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
leg = ["k=5","k=7", "k=9"]
#plt.plot(ns, sequential)
plt.plot(ns[0:-1], sp)
plt.xlabel("n")
plt.ylabel("Ts/Tp")
plt.legend(leg,loc="lower right")
plt.title("PyOpenCL Speedup")



plt.show()
