*********************************
Solving the Schroedinger Equation
*********************************

schrodinger_solve solves the one dimensional stationary Schroedinger equation for given data points.
This was done by first reading the input data and then solving the eigenvalue problem with a tridiagonal matrix as well as normalizing the wavefunctions.
Before the equation could be solved the data points for the potential had to be interpolated.
The uncertainties and the expected values were also calculated.
In the end, the interpolated potential, the normalized wavefunctions, the eigenvalues, the expected values, and the uncertainties were saved in specified data sheets.

**Usage**

.. code-block:: text

   schrodinger_solve [-h] [-o OUTPUT_DIR] filename

**Command line options**

.. code-block:: text

	positional arguments:
	  filename              File describing the system to solve

	options:
	  -h, --help            show this help message and exit
	  -d DIRECTORY, --directory DIRECTORY
	                        Input and Output directory for the results
