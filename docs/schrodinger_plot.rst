*************************************************
Plotting the Results of the Schroedinger Equation
*************************************************

schrodinger_plot plots the interpolated potential and normalized wavefunctions over the lattice, eigenvalues as horizontal line and the expected values for the position operator in one figure.
In another figure the eigenvalues and the uncertainty of the positional measurement are plotted. 
These two plots are combined as subplots into one figure.

**Usage**

.. code-block:: text

   schrodinger_plot.py [-h] [-d DIRECTORY] [-s SHOW] [-e EXPORT] [-f FACTOR] [-x XLIMITS] [-y YLIMITS]

**Command line options**

.. code-block:: text

  -h, --help            show a help message
  -d DIRECTORY --directory DIRECTORY
                        the path where the pdf should be saved (default: None)
  -s SHOW --show SHOW   Boolean, if True the plot is shown directly (default:
                        False)
  -e EXPORT --export EXPORT
                     	Boolean, if True the plot is exported as a pdf
                        (default: True)
  -f FACTOR --factor FACTOR
                     	Float, Factor to scale wavefunctions (default: 1.0)
  -x XLIMITS --xlimits XLIMITS	
                        Limits of the x-axis of the wavefunction plot. 
						      None or tuple(float, float) of shape (x_min, x_max). 
						      (default: None)
  -y YLIMITS --ylimits YLIMITS
                        Limits of the shared y-axis. None or tuple(float, float)
						      of shape (y_min, y_max). (default: None)
 