import numpy as np
import scipy as sp


def import_input(directory="./"):
    """
    Returns lines from schrodinger.inp.
    
    :param directory: Optional parameter to set if input file is not located in root directory.

    :return: List with fit parameters.
    """
    raw_input_data = []
    try:
        input_file = open(directory + "schrodinger.inp", "r")
        
    except FileNotFoundError:
        print("Could not open {}".format(directory + "schrodinger.inp")) 

    else:
        for line in input_file:
            line = line.split("\t")[0]
            line = line.split("\n")[0]
            raw_input_data.append(line)   
        input_file.close()
    return raw_input_data

def save_variables(raw_input_data):
    """
    Seperates list into variables.

    :param raw_input_data: Parameter from which to take the variables.

    :return: Variables
    """
    m = float(raw_input_data[0])
    line2 = raw_input_data[1].split(" ")
    xMin = float(line2[0])
    xMax = float(line2[1])
    nPoint = int(line2[2])
    line3 = raw_input_data[2].split(" ")
    firstEV = int(line3[0])-1
    lastEV = int(line3[1])-1
    interp_type = raw_input_data[3]
    num_interp_points = int(raw_input_data[4])
    potential_points = []
    xPot = []
    yPot = []
    for i in range(5, 5+num_interp_points):
        potential_points.append(raw_input_data[i].split(" "))
        xPot.append(float(potential_points[i-5][0]))
        yPot.append(float(potential_points[i-5][1]))
    deg = len(xPot)-1

    return m, xMin, xMax, nPoint, firstEV, lastEV, interp_type, num_interp_points, deg, xPot, yPot

raw_input_data = import_input("./")

m, xMin, xMax, nPoint, firstEV, lastEV, interp_type, num_interp_points, deg, xPot, yPot = save_variables(raw_input_data)

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
        text = f'{gitter[i]}' f' {Potential[i]} \n'
        potentialdat.write(text)

with open('energies.dat', "w") as energiesdat:
    for i in range(len(eigVal)):
        text = f'{eigVal[i]} \n'
        energiesdat.write(text)

with open('wavefuncs.dat', "w") as wavefuncsdat:
    for i in range(nPoint):
        text = f'{gitter[i]} ' 
        for ii in range(len(eigVal)):
            text += f'{eigVec[i][ii]} '
        text += f'\n'
        wavefuncsdat.write(text)



def expval():
    expvalue = []
    expvalQuad = []
    for i in range(len(eigVal)):
        expvalue.append( delta * np.sum( eigVec[i, :] * gitter[i] * eigVec[i, :] ) )
        #expvalue.append( ( expvalue[i] ** 2) )
        expvalQuad.append( delta * np.sum( eigVec[i, :] * gitter[i] ** 2 * eigVec[i, :] ) )
    expvalue = np.array(expvalue)
    expvalQuad = np.array(expvalQuad)
    uncertainty = ( np.sqrt( ( expvalQuad - expvalue ** 2 ) ) )
    return uncertainty, expvalue, expvalQuad

uncertainty, expvalue, expvalQuad = expval()

with open('expvalues.dat', "w") as expvaldat:
    for i in range(len(expvalue)):
        text = f'{expvalue[i]} {uncertainty[i]}\n'
        expvaldat.write(text)

