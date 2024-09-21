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
