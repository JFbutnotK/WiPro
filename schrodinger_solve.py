import numpy as np
import scipy as sp
import matplotlib as plt
#import pytest 
#solving the Schroedinger equation


m = 1.0
xMin = -2.0
xMax = 2.0
nPoint = 1999


def a():
    gitter = np.linspace(xMin, xMax, nPoint)
    delta = 1
    abkurzung = 1 / ( m * delta ** 2 )
    return gitter



print(a())

