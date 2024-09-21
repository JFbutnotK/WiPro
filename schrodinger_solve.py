import numpy as np
import scipy as sp
import matplotlib as plt
#import pytest 
#solving the Schroedinger equation


m = 2.0
xMin = -2.0
xMax = 2.0
nPoint = 1999
interp_type = 'linear'
xPot = [-2.0, -0.5, -0.5, 0.5, 0.5, 2.0]
yPot = [0.0, 0.0, -10.0, -10.0, 0.0, 0.0]
deg = len(xPot)-1
firstEV = 0
lastEV = 15


def abkurzung():
    gitter = np.linspace(xMin, xMax, nPoint)
    delta = np.abs( gitter[1] - gitter[0] )
    a = 1 / ( m * delta ** 2 )
    return a, gitter

a, gitter = abkurzung()

def PotentialInterpolation():
    if interp_type == 'linear':
        Potential = np.interp(gitter, xPot, yPot)

    elif interp_type == 'polynomial':
        PolyFit = np.polyfit(xPot, yPot, deg)
        Potential = np.polyval(PolyFit, gitter)

    elif interp_type == 'cspline':
        CSpline = sp.interpolate.CubicSpline(xPot, yPot)
        Potential = CSpline(gitter)

    else:
        raise ValueError('The used interpolation type is not supported by this program. Supported types are: linear, polynomial, cspline.')

    return(Potential)

Potential = PotentialInterpolation()

NebenDiagonale = [- 1 / 2 * a] * ( nPoint - 1 )
HauptDiagonale = a + Potential

eigVal, eigVec = sp.linalg.eigh_tridiagonal(HauptDiagonale, NebenDiagonale, select = 'i', select_range = (firstEV, lastEV))

print(eigVal)