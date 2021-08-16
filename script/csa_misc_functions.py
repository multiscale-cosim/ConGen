import numpy as np
import csa

def getArray(cset, x=30, y=30):
    a = np.zeros ((x, y))
    for (i, j) in csa.elementary.cross (xrange (x), xrange (y)) * cset:
        a[i,j] += 1.0
    return a