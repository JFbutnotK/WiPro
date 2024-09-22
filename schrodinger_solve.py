"""
Modules used for linear algebra and interpolation.
#"""
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
        input_file = open(directory + "schrodinger.inp", "r", encoding="utf-8")

    except FileNotFoundError:
        print("blob")
        #Überarbeitung

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
    xmin = float(line2[0])
    xmax = float(line2[1])
    npoint = int(line2[2])
    line3 = raw_input_data[2].split(" ")
    firstev = int(line3[0])-1
    lastev = int(line3[1])-1
    int_type = raw_input_data[3]
    num_int_points = int(raw_input_data[4])
    potential_points = []
    x_pot = []
    y_pot = []
    for j in range(5, 5+num_interp_points):
        potential_points.append(raw_input_data[j].split(" "))
        xpot.append(float(potential_points[j-5][0]))
        ypot.append(float(potential_points[j-5][1]))
    degree = len(xpot)-1

    return m, xmin, xmax, npoint, firstev, lastev, int_type, num_int_points, degree, x_pot, y_pot

raw_data = import_input("./")

mass, x_min, x_max, n_point, first_ev, last_ev, interp_type, num_interp_points, deg, xpot, ypot = save_variables(raw_data)

def abkurzung():
    """
    Calculates the lattice points, the distance between neighbouring points.

    :param :

    :return: A factor using the mass and the distance, array with the lattice points, and the distance between neighbouring lattice points.
    """
    lattice = np.linspace(x_min, x_max, n_point)
    deriv = np.abs( gitter[1] - gitter[0] )
    abk = 1 / ( mass * delta ** 2 )
    return abk, lattice, deriv

a, gitter, delta = abkurzung()



def interpolation():
    """
    Interpolates the potential points given in schrodinger.inp.
    
    :param :

    :return: Array with interpolated potential.
    """
    if interp_type == 'linear':
        potential = np.interp(gitter, xpot, ypot)

    elif interp_type == 'polynomial':
        poly_fit = np.polyfit(xpot, ypot, deg)
        potential = np.polyval(poly_fit, gitter)

    elif interp_type == 'cspline':
        c_spline = sp.interpolate.CubicSpline(xpot, ypot)
        potential = c_spline(gitter)

    else:
        raise ValueError('The used interpolation type is not supported by this program. Supported types are: linear, polynomial, cspline.')

    return potential

potenzial = interpolation()



def schrodinger_eq():
    """
    Calculates stationary Schroedinger equation for given paramaters as eigenvalue problem.
    
    :param :

    :return: Arrays with eigenvalues and eigenvectors.
    """
    neben_diagonale = [- 1 / 2 * a] * ( n_point - 1 )
    haupt_diagonale = a + potenzial
    eigval, eigvec = sp.linalg.eigh_tridiagonal(haupt_diagonale, neben_diagonale, select = 'i', select_range = (first_ev, last_ev))
    for h in range(len(eigval)):
        eigvec[:, h] /= np.sqrt( delta * np.sum( np.abs( eigvec[:, h] ) ** 2 ) )
    return eigval, eigvec

eig_val, eig_vec = schrodinger_eq()



with open('potential.dat', "w", encoding="utf-8") as potentialdat:
    for f in range(n_point):
        text = f'{gitter[f]}' f' {potenzial[f]} \n'
        potentialdat.write(text)

with open('energies.dat', "w", encoding="utf-8") as energiesdat:
    for p in range(len(eig_val)):
        text = f'{eig_val[p]} \n'
        energiesdat.write(text)

with open('wavefuncs.dat', "w", encoding="utf-8") as wavefuncsdat:
    for n in range(n_point):
        text = f'{gitter[n]} '
        for ii in range(len(eig_val)):
            text += f'{eig_vec[n][ii]} '
        text += '\n'
        wavefuncsdat.write(text)



def expval():
    """ 
    Calculates the expected values for the eigen problem as well as the uncertainties. 

    :param :

    :return: Arrays with uncertainties and expected values.
    """
    expvalue = []
    expval_quad = []
    for k in range(len(eig_val)):
        expvalue.append( delta * np.sum( eig_vec[k, :] * gitter[k] * eig_vec[k, :] ) )
        expval_quad.append( delta * np.sum( eig_vec[k, :] * gitter[k] ** 2 * eig_vec[k, :] ) )
    expvalue = np.array(expvalue)
    expval_quad = np.array(expval_quad)
    uncertainty = ( np.sqrt( ( expval_quad - expvalue ** 2 ) ) )
    return uncertainty, expvalue

uncert, exp_value = expval()

with open('expvalues.dat', "w", encoding="utf-8") as expvaldat:
    for i in range(len(exp_value)):
        text = f'{exp_value[i]} {uncert[i]}\n'
        expvaldat.write(text)
