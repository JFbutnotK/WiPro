"""
Module numpy is used for evaluating and using arrays
Module pyplot is used for plotting the results and saving them
"""
import numpy as np
from matplotlib import pyplot as plt

directory = input('Please enter the directory from which the .dat files should be taken. \n'
                  +'If the current directory is correct please enter \'./\'\n')


raw_potential_data = []
try:
    potential_file = open(directory + "potential.dat", "r", encoding="utf-8")
except FileNotFoundError as exc:
    raise ValueError("potential.dat could not be found in this directory.") from exc

for line in potential_file:
    line = line.split("\n")[0]
    raw_potential_data.append(line)
potential_file.close()

potential = []

for i, data in enumerate(raw_potential_data):
    line = data.split(" ")
    potential.append(float(line[1]))


energies = []
try:
    energies_file = open(directory + "energies.dat", "r", encoding="utf-8")

except FileNotFoundError as exc:
    raise ValueError("energies.dat could not be found in this directory.") from exc

for line in energies_file:
    line = line.split("\n")[0]
    energies.append(float(line))
energies_file.close()



raw_wavefunc_data = []
try:
    wavefuncs_file = open(directory + "wavefuncs.dat", "r", encoding="utf-8")
except FileNotFoundError as exc:
    raise ValueError("wavefuncs.dat could not be found in this directory.") from exc

for line in wavefuncs_file:
    line = line.split("\n")[0]
    raw_wavefunc_data.append(line)
wavefuncs_file.close()

x = []
wavefuncs = np.empty((len(energies), len(potential)))

for k in range(len(raw_wavefunc_data)):
    line = raw_wavefunc_data[k].split(" ")
    x.append(float(line[0]))

    for l in range(len(energies)):
        wavefuncs[l][k] = float(line[l+1])


raw_expvalues_data = []
try:
    expvalues_file = open(directory + "expvalues.dat", "r", encoding="utf-8")
except FileNotFoundError as exc:
    raise ValueError("expvalues.dat could not be found in this directory.") from exc


for line in expvalues_file:
    line = line.split("\n")[0]
    raw_expvalues_data.append(line)
expvalues_file.close()

pos_exp_val = []
uncert = []

for i in range(len(energies)):
    line = raw_expvalues_data[i].split(" ")
    pos_exp_val.append(float(line[0]))
    uncert.append(float(line[1]))




def plot_results():
    """
    This function plots the interpolated potential and wavefunctions over the lattice, eigenvalues 
    as horizontal line and the expected values for the position operator in one figure.
    In another figure the eigenvalues and the uncertainty of the positional measurement are plotted. 
    These two plots are combined as subplots into one figure.

    :param:

    :return: schrodinger_results.pdf if the save option is selected.
    """
    plt.figure()
    ax1 = plt.subplot(1, 2, 1)

    colours = ['b', 'r']
    plt.plot(x, potential, c='black')
    plt.hlines(energies, 1.1*min(x), 1.1*max(x), colors='grey', linestyle='-')
    for m, func in enumerate(wavefuncs):
        plt.plot(x, func+energies[m], c=colours[m % len(colours)])
    plt.scatter(pos_exp_val, energies, c='green', marker='x')
    plt.xlabel('x [Bohr]')
    plt.ylabel('Energy [Hartree]')
    plt.title('Potential, eigenstates, ⟨x⟩')
    plt.xlim(1.1*min(x), 1.1*max(x))

    plt.subplot(1, 2, 2, sharey=ax1)
    plt.hlines(energies, 0, 1.1*max(uncert), colors='grey', linestyle='-')
    plt.scatter(uncert, energies,  c='violet', marker='+')
    plt.xlabel('[Bohr]')
    plt.title(r'$\sigma_x$')
    plt.xlim(0, 1.1*max(uncert))

    display=input('Please select \'show\' or \'save\' to select if results are shown or saved.\n')

    if display == 'show':
        plt.show()
    elif display == 'save':
        plt.savefig('schrodinger_results.pdf', dpi=300)
    else:
        print('Invalid input. Please try again.')
plot_results()
