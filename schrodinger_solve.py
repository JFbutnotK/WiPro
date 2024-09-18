import numpy as np
import scipy as sp
import matplotlib as plt
#import pytest 

#read input file

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


raw_input_data = import_input("./")
print(raw_input_data)