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
import Queue
import csv
import re
import os

TESTPATH = "/home/hlocal/repos/sgdi/P2/k-NN/iris_test.csv"
K = 5

def toFloat(string):
    """
    Function: toFloat
    Descrp: Convierte los string posibles a float.
    Args:
    -> string: string a convertir
    Return:
    -> float (o string si no se ha podido convertir)
    """

    aux = string
    try:
        aux = float(string)
    except:
        aux = string
    return aux


def isNotFloat(elem):
    """
    Function: isNotFloat
    Descrp: Comprueba si el argumento es float.
    Args:
    -> elem: argumento a comprobar
    Return:
    -> booleano inidicando si es float
    """

    try:
        a = float(elem)
    except:
        return True
    return False


def read_file( filename = "iris_test.csv" ):
    """
    Function: read_file
    Descrp: Lee el archivo linea a linea y devuelve las instancias.
    Args:
    -> filename: CSV Nombre del archivo a leer
    Return:
    -> Lista de las instancias.
    """

    infile = open(filename,"r")
    reader = csv.reader(infile)
    rows = []
    for row in reader:
        tmp = [toFloat(w) for w in row]
        rows.append(tmp)
    return rows[1:]


def mode(l):
    """
    Function: mode
    Descrp: Devuelve la moda de la lista pasada.
    Args:
    -> l: lista
    Return:
    -> la moda de la lista
    """

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


    def mapper_init(self):
        """
        Parsea el fichero de test y lo almacena como atributo
        de la clase.
        Prepara el diccionario que se va a utilizar para guardar
        las K instancias más próximas en este nodo map a cada
        instancia.
        """
        self.testset = read_file(TESTPATH)
        self.dic = {}

        for t in self.testset:
            self.dic[str(t)] = []


    def mapper(self, key, line):
        
        w = line.split(',')
        if isNotFloat(w[0]):
            # Saltamos la primera linea del archivo
            return
        # convierte cada atributo de la instancia en float si puede
        w = map(toFloat,w)
        for t in self.testset:
            # por cada instancia en el test calcula la distancia
            # con la instancia a evaluar.
            dis = distance.euclidean(t[:-1],w[:-1])
            if len(self.dic[str(t)]) < K:
                # si la lista de instancias tiene espacio añadimos la nueva
                self.dic[str(t)].append((dis,w[-1]))
            elif self.dic[str(t)][-1][0] > dis:
                # si no tiene espacio y la distancia actual 
                # es menor que la mayor de la lista
                self.dic[str(t)].append((dis,w[-1]))
                # ordenamos y nos quedamos con los K primeros
                self.dic[str(t)] = sorted(self.dic[str(t)])[:K]


    def mapper_final(self):
        for t in self.testset:
            # por cada instancia del test
            key = str(t)
            # emitimos los K (o menos de K) instancias más próximas
            for inst in self.dic[key]:
                yield (t, inst)


    def reducer(self, key, values):
        # ordenamos todas las instancias por su primera componente
        # es decir, la distancia, y nos quedamos con los K primeros
        par = sorted(values)[:K]
        # nos quedamos solo con las instancias
        par = [p[1] for p in par]
        # y publicamos la moda de la lista
        yield key, mode(par)


if __name__ == '__main__':
    MRWordCount.run()
