from mapclassify import Fisher_Jenks, PFisher_Jenks, PFisher_Jenks_MP, PFisher_Jenks_PP
import numpy as np

dat = np.random.rand(2000)

o1 = Fisher_Jenks(dat)

o2 = PFisher_Jenks(dat)

o3 = PFisher_Jenks_MP(dat)

o4 = PFisher_Jenks_PP(dat)
