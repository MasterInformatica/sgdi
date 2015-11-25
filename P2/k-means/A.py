# -*- coding: utf-8 -*-
import csv
from scipy.spatial import distance

"""
Function: toFloat
Args:
-> string: string to be converted
Return:
-> float or string if we can not convert
"""
def toFloat(string):
    aux = string
    try:
        aux = float(string)
    except:
        aux = string
    return aux

"""
Function: read_file
Args:
-> filename: CSV File name to be read.
Return:
-> List of instance for each file line.
"""
def read_file( filename = "customers.csv" ):
    infile = open(filename,"r")
    reader = csv.reader(infile)
    rows = []
    for row in reader:
        tmp = [toFloat(w) for w in row]
        rows.append(tmp)
    return rows[1:]


print read_file()
