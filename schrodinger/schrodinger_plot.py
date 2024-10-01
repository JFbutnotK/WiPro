"""
This module plots the data that is received when using schrodinger_solve.
"""
import argparse
import numpy as np
from matplotlib import pyplot as plt


def load_files(directory):
    """
    Loads data from respecetive files and prepares it for plotting.

    :param directory: CommandLine input to be able to provide a directory.

    :return: Dictionary to save all variables to.
    """

    potential_data = np.loadtxt(directory + '/potential.dat')
    energies = np.loadtxt(directory + '/energies.dat')
    wavefuncs_data = np.loadtxt(directory + '/wavefuncs.dat')
    expvalues_data = np.loadtxt(directory + '/expvalues.dat')

    data_dict = {
        'potential': potential_data[:, 1],
        'energies': energies,
        'expvalues': expvalues_data[:, 0],
        'uncertainty': expvalues_data[:, 1],
        'lattice': wavefuncs_data[:, 0],
        'wavefuncs': wavefuncs_data[:, 1:].transpose()
    }

    return data_dict


def plot_results(data_dict, args):
    """
    This function plots the interpolated potential and wavefunctions over the lattice, eigenvalues 
    as horizontal line and the expected values for the position operator in one figure.
    In another figure the eigenvalues and the uncertainty of the positional measurement are plotted. 
    These two plots are combined as subplots into one figure.

    :param data_dict: Dictionary all variables used for plotting a stored in.
    :param args: Set of CommandLine inputs to change the directory of saved files, decide whether to show and/or save the figure, factor to scale wavefunctions, x- and y-limits for the figure

    :return: schrodinger_results.pdf if the save option is selected.
    """

    energies = data_dict['energies']
    x = data_dict['lattice']
    potential = data_dict['potential']
    wavefuncs = data_dict['wavefuncs']
    pos_exp_val = data_dict['expvalues']
    uncert = data_dict['uncertainty']

    plt.figure()
    ax1 = plt.subplot(1, 2, 1)

    colours = ['b', 'r']
    plt.plot(x, potential, c='black')
    plt.hlines(energies, 1.1*min(x), 1.1*max(x), colors='grey', linestyle='-')
    for i, func in enumerate(wavefuncs):
        plt.plot(x, (args.factor*func)+energies[i], c=colours[i % len(colours)])
    plt.scatter(pos_exp_val, energies, c='green', marker='x')
    plt.xlabel('x [Bohr]')
    plt.ylabel('Energy [Hartree]')
    plt.title('Potential, eigenstates, ⟨x⟩')
    if args.xlimits is None:
        plt.xlim(1.1*min(x), 1.1*max(x))
    else:
        plt.xlim(args.xlimits)

    if args.ylimits is None:
        plt.ylim(min(potential), max(energies)+abs(max(energies)))
    else:
        plt.ylim(args.ylimits)

    plt.subplot(1, 2, 2, sharey=ax1)
    plt.hlines(energies, 0, 1.1*max(uncert), colors='grey', linestyle='-')
    plt.plot(uncert, energies,  c='violet', marker='+', markersize = 10, ls = '')
    plt.xlabel('[Bohr]')
    plt.title(r'$\sigma_x$')
    plt.xlim(0, 1.1*max(uncert))


    if args.export:
        plt.savefig(args.directory + '/schrodinger_results.pdf', dpi=300)
    if args.show:
        plt.show()

    plt.close()


def main():
    """
    Program entry point
    
    """
    _description = 'Plots solutions of schrodinger_solve.py.'
    parser = argparse.ArgumentParser(description=_description)
    message = 'path: Directory of the data and to which the plot might be saved.  (default: .)'
    parser.add_argument('-d', '--directory', default='.', help=message)
    message = 'bool: Show figure?  (default: False)'
    parser.add_argument('-s', '--show', default=False, help=message, type=bool)
    message = 'bool: Export figure?  (default: True)'
    parser.add_argument('-e', '--export', default=True, help=message, type=bool)
    message = 'float: Factor to scale wavefunctions.  (default: 1)'
    parser.add_argument('-f', '--factor', default=1, help=message, type=float)
    message = 'Limits of the x-axis of the wavefunction plot. None or tuple(float, float) of shape (x_min, x_max). (default: None)'
    parser.add_argument('-x', '--xlimits', default=None, help=message, nargs='+')
    message = 'Limits of the shared y-axis. None or tuple(float, float) of shape (y_min, y_max). (default: None)'
    parser.add_argument('-y', '--ylimits', default=None, help=message, nargs='+')
    args = parser.parse_args()

    data_dict = load_files(args.directory)
    plot_results(data_dict, args)


if __name__ == "__main__":
    main()
