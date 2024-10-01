"""
Solves the time-independent 1-d Schrödinger equation for given potentials.
"""
import argparse
import os
import numpy as np
import scipy as sp



def import_input(directory):
    """
    Returns lines from schrodinger.inp.
    
    :param directory: Optional parameter to set if input file is not located in root directory.

    :return: List with fit parameters.
    """
    raw_input_data = []
    input_file = open(os.path.join(directory, "schrodinger.inp"), "r", encoding="utf-8")

    for line in input_file:
        line = line.split("#")[0]
        line = ' '.join(line.split())
        raw_input_data.append(line)
    input_file.close()

    return raw_input_data


def save_variables(raw_input_data):
    """
    Seperates list into variables.

    :param raw_input_data: Parameter from which to take the variables.

    :return: Variables in Dictionary
    """
    m = float(raw_input_data[0])
    line2 = raw_input_data[1].split()
    xmin = float(line2[0])
    xmax = float(line2[1])
    npoint = int(line2[2])
    line3 = raw_input_data[2].split(" ")
    firstev = int(line3[0])-1
    lastev = int(line3[1])-1
    int_type = raw_input_data[3].replace(" ","").replace("\t","")
    num_int_points = int(raw_input_data[4])
    potential_points = []
    x_pot = []
    y_pot = []
    for j in range(5, 5+num_int_points):
        potential_points.append(raw_input_data[j].split(" "))
        x_pot.append(float(potential_points[j-5][0]))
        y_pot.append(float(potential_points[j-5][1]))
    degree = len(x_pot)-1

    data_dict = {'m': m,
              'x_min': xmin, 
              'x_max': xmax, 
              'n_point': npoint, 
              'first_ev': firstev, 
              'last_ev': lastev, 
              'int_type': int_type, 
              'num_int_points': num_int_points, 
              'deg': degree, 
              'xpot': x_pot, 
              'ypot': y_pot
              }
    return data_dict


def abbrev(data_dict):
    """
    Calculates the lattice points, the distance between neighbouring points.

    :param data_dict: Dictionary to store all variables.

    :return: Dictionary to store all variables.
    """
    x_min=data_dict['x_min']
    x_max=data_dict['x_max']
    n_point=data_dict['n_point']
    mass=data_dict['m']
    lattice = np.linspace(x_min, x_max, n_point)
    deriv = np.abs( lattice[1] - lattice[0] )
    abk = 1 / ( mass * deriv ** 2 )

    data_dict['a']=abk
    data_dict['lat']=lattice
    data_dict['delta']=deriv

    return data_dict


def interpolation(data_dict):
    """
    Interpolates the potential points given in schrodinger.inp.
    
    :param data_dict: Dictionary to store all variables.

    :return: Dictionary to store all variables.
    """

    interp_type = data_dict['int_type']
    lat = data_dict['lat']
    xpot = data_dict['xpot']
    ypot = data_dict['ypot']
    deg = data_dict['deg']

    if interp_type == 'linear':
        potential = np.interp(lat, xpot, ypot)

    elif interp_type == 'polynomial':
        poly_fit = np.polyfit(xpot, ypot, deg)
        potential = np.polyval(poly_fit, lat)

    elif interp_type == 'cspline':
        c_spline = sp.interpolate.CubicSpline(xpot, ypot, bc_type = 'natural')
        potential = c_spline(lat)

    else:
        raise ValueError(f'The used interpolation type is not supported by this program. Supported types are: linear, polynomial, cspline. Momentaner type ist: {interp_type}!')

    data_dict['pot'] = potential
    return data_dict


def schrodinger_eq(data_dict):
    """
    Calculates stationary Schroedinger equation for given paramaters as eigenvalue problem.
    
    :param data_dict: Dictionary to store all variables.

    :return: Dictionary to store all variables.

    """
    n_point = data_dict['n_point']
    a = data_dict['a']
    pot = data_dict['pot']
    first_ev = data_dict['first_ev']
    last_ev = data_dict['last_ev']
    delta = data_dict['delta']

    off_diagonal = [- 1 / 2 * a] * ( n_point - 1 )
    main_diagonal = a + pot
    eigval, eigvec = sp.linalg.eigh_tridiagonal(main_diagonal, off_diagonal, select = 'i', select_range = (first_ev, last_ev))
    for h in range(len(eigval)):
        eigvec[:, h] /= np.sqrt( delta * np.sum( np.abs( eigvec[:, h] ) ** 2 ) )

    data_dict['eigval'] = eigval
    data_dict['eigvec'] = eigvec
    return data_dict


def expval(data_dict):
    """ 
    Calculates the expected values for the eigen problem as well as the uncertainties. 

    :param data_dict: Dictionary to store all variables.

    :return: Arrays with uncertainties and expected values.
    """
    eigval = data_dict['eigval']
    eigvec = data_dict['eigvec']
    lat = data_dict['lat']
    delta = data_dict['delta']

    expvalue = []
    expval_quad = []
    for k in range(len(eigval)):
        expvalue.append( delta * np.sum( eigvec[k, :] * lat[k] * eigvec[k, :] ) )
        expval_quad.append( delta * np.sum( eigvec[k, :] * lat[k] ** 2 * eigvec[k, :] ) )
    expvalue = np.array(expvalue)
    expval_quad = np.array(expval_quad)
    uncertainty = ( np.sqrt( ( expval_quad - expvalue ** 2 ) ) )

    data_dict['uncert'] = uncertainty
    data_dict['exp_value'] = expvalue
    return data_dict


def save_data(data_dict):
    """
    Saves results into respective files.

    :param data_dict: Dictionary to store all variables.
    
    """

    pot = data_dict['pot']
    lat = data_dict['lat']
    n_point = data_dict['n_point']
    eigval = data_dict['eigval']
    eigvec = data_dict['eigvec']
    exp_value = data_dict['exp_value']
    uncert = data_dict['uncert']

    with open('potential.dat', "w", encoding="utf-8") as potentialdat:
        for f in range(n_point):
            text = f'{lat[f]}' f' {pot[f]} \n'
            potentialdat.write(text)

    with open('energies.dat', "w", encoding="utf-8") as energiesdat:
        for p in range(len(eigval)):
            text = f'{eigval[p]} \n'
            energiesdat.write(text)

    with open('wavefuncs.dat', "w", encoding="utf-8") as wavefuncsdat:
        for n in range(n_point):
            text = f'{lat[n]} '
            for ii in range(len(eigval)):
                text += f'{eigvec[n][ii]} '
            text += '\n'
            wavefuncsdat.write(text)

    with open('expvalues.dat', "w", encoding="utf-8") as expvaldat:
        for i in range(len(exp_value)):
            text = f'{exp_value[i]} {uncert[i]}\n'
            expvaldat.write(text)



def main():
    """
    Program entry point
    """
    _description = 'Solves time-independant schroedinger equation from input file.'
    parser = argparse.ArgumentParser(description=_description)
    message = 'directory  (default: .)'
    parser.add_argument('-d', '--directory', default='.', help=message)
    args = parser.parse_args()


    raw_data = import_input(args.directory)
    data_dict = save_variables(raw_data)
    abbrev(data_dict)
    interpolation(data_dict)
    schrodinger_eq(data_dict)
    expval(data_dict)
    save_data(data_dict)


if __name__ == "__main__":
    main()
