# -*- coding: utf-8 -*-
"""
 Sistemas de gestion de datos y de la informacion 
 Practica 2
 Luis Maria Costero Valero 
 Jesus Javier Domenech Arellano 

 Nosotros, Luis M. Costero y Jesus Domenech, declaramos la autoria completa de este documento. 

"""


from mrjob.job import MRJob
from scipy.spatial import distance
import csv
import re
import os

TESTPATH = "/home/friker/Uni/Master/SGDI/P2/k-NN/iris_test.csv"
K = 5

"""
Function: toFloat
Descr: 
Input:
  string: string to be converted
Return:
  float or string if we can not convert
"""
def toFloat(string):
    aux = string
    try:
        aux = float(string)
    except:
        aux = string
    return aux

"""
Function: isNotFloat
Descr: 
Input:
  string: string to be converted
Return:
  False is float True otherwise
"""
def isNotFloat(elem):
    try:
        a = float(elem)
    except:
        return True
    return False

"""
Function: read_file
Descr:
Input:
   filename: CSV File name to be read.
Return:
   List of instance for each file line.
"""
def read_file( filename = "iris_test.csv" ):
    infile = open(filename,"r")
    reader = csv.reader(infile)
    rows = []
    for row in reader:
        tmp = [toFloat(w) for w in row]
        rows.append(tmp)
    return rows[1:-1]



def mode(l):
    """ Devuelve la moda de la lista pasada """
    max_num = -1
    moda = None
    dic={}

    for p in l:
        if not p in dic:
            dic[p] = 1
        else:
            dic[p] += 1

        if max_num < dic[p]:
            max_num = dic[p]
            moda = p

    return moda


class MRWordCount(MRJob):

    def mapper(self, key, line):
        w = line.split(',')
        if isNotFloat(w[0]):
            return
        w = map(toFloat,w)
        testset = read_file(TESTPATH)
        for t in testset:
            dis = distance.euclidean(t[:-1],w[:-1])
            yield t,(dis,w[-1])


    def combiner(self, key, values):
        vals = sorted(values)[:K]
        for w in vals:
            yield key, w

    # Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        par = sorted(values)[:K]
        par = [p[1] for p in par]
        yield key, mode(par)


if __name__ == '__main__':
    MRWordCount.run()
