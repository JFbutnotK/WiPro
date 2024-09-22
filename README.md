# Solving and printing the Schroedinger equation

This program tries to solve the schroedinger equation for given input data. This data can be managed manually in a document called 'schrodinger.input'.

The input sheet should have the the mass, the first and last x value of the lattice as well as how many points should be distributed between them, the first and last eigenvalue in output, the interpolation type where only 'linear', 'polynomial' or 'cspline' may be chosen, the number of interpolation points, and the x and y declarations for the potential in the xy-format and one pair per line. All values in one line should be separated by one space.
The sheet should follow the format:

mass
first and last value for lattice and number of points
first and last eigenvalue
interpolation type
number of interpolation points
xy declarations for potential

After successfully saving the data in 'schrodinger.inp' the code 'schrodinger_solve.py' may be run. Please ensure that the 'schrodinger.inp' file is in the same repository as the code 'schrodinger_solve.py'.
To get the visual results please use the code 'schrodinger_plot.py'.
