from mapclassify import Fisher_Jenks_1, PFisher_Jenks, PFisher_Jenks_MP
from mapclassify import PFisher_Jenks_PP
from mapclassify_V2 import PFisher_Jenks_PP as PFisher_Jenks_PP2
import numpy as np

if __name__ == "__main__":
    dat = np.random.rand(2000)

    print "Sequential\n"
    o1 = Fisher_Jenks_1(dat)
    print o1

    print "PyOpenCL\n"
    o2 = PFisher_Jenks(dat)
    print o2

    print "Multiprocessing\n"
    o3 = PFisher_Jenks_MP(dat)
    print o3
    
    print "Parallel Python\n"
    o4 = PFisher_Jenks_PP(dat)
    print o4

    print "Parallel Python Modified\n"
    o5 = PFisher_Jenks_PP2(dat)
    print o5
