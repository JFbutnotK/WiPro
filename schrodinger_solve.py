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
lastEV = 2


def abkurzung():
    gitter = np.linspace(xMin, xMax, nPoint)
    delta = np.abs( gitter[1] - gitter[0] )
    a = 1 / ( m * delta ** 2 )
    return a, gitter, delta

a, gitter, delta = abkurzung()



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



def SchrodingerEq():
    NebenDiagonale = [- 1 / 2 * a] * ( nPoint - 1 )
    HauptDiagonale = a + Potential
    eigVal, eigVec = sp.linalg.eigh_tridiagonal(HauptDiagonale, NebenDiagonale, select = 'i', select_range = (firstEV, lastEV))
    for i in range(len(eigVal)):
        eigVec[:, i] /= np.sqrt( delta * np.sum( np.abs( eigVec[:, i] ) ** 2 ) )
    return eigVal, eigVec

eigVal, eigVec = SchrodingerEq()



with open('potential.dat', "w") as potentialdat:
    for i in range(nPoint):
        text = f'{gitter[i]} \t {Potential[i]} \n'
        potentialdat.write(text)

with open('energies.dat', "w") as energiesdat:
    for i in range(len(eigVal)):
        text = f'{eigVal[i]} \n'
        energiesdat.write(text)

with open('wavefuncs.dat', "w") as wavefuncsdat:
    for i in range(nPoint):
        text = f'{gitter[i]} \t'
        for ii in range(len(eigVal)):
            text += f'{eigVec[i][ii]} \t'
        text += f'\n'
        wavefuncsdat.write(text)