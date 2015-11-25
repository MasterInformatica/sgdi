# -*- coding: utf-8 -*-

import csv
import pprint
from scipy.spatial import distance

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
    return rows[1:]



"""
Function: knn
Descr: 
Input:
   k: number of neighbours 
   i: instance to be analiZ?????????????
   c: trainset
Return:
   a string who indicates the predicted class of i
"""
def knn ( k, i , c ):
    clases = clase_kvecinos_cercanos(k,i,c)
    return mode(clases)



#TODO: Documentar
"""
Function:
Descr:
Input:
   k: 
   i: 
   c: 
Return:

"""
def clase_kvecinos_cercanos(k, i, c):
    """ Devuelve las k clases de lso k vecinos más cercanos """

    #si tienen el mismo tamaño significa que i tiene la clase puesta
    if len(i) == len(v):
        distances = [ distance.euclidean(i[:-1],v[:-1]) for v in c]
    #sino es que no tiene la clase en la ultima
    else:
        distances = [ distance.euclidean(i,v[:-1]) for v in c]

    #creamos las parejas (distancia, clase)
    par=[]
    for i in range(0,len(c)):
        par += [(distances[i], c[i][-1])]
    
    #nos quedamos con las k instancias con distancia menor
    par= sorted(par)[:k]
    #y solamente con la clase, sin las distancias
    par = [p[1] for p in par]

    return par
    

#TODO: Documentar
"""
Function:
Descr:
Input:
   k: 
   i: 
   c: 
Return:

"""
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



"""
Function: test
Descr:
Input:
   k: number of neighbours
   trainset: 
   testset: 
Return:

"""
def test( k, trainset, testset):
    clasificacion = [knn(k,x,trainset)    for x in testset]
    numAciertos = 0

    for i in range(0, len(testset)):
        print clasificacion[i] ,",", testset[i][-1]
        if clasificacion[i] == testset[i][-1]:
            numAciertos += 1


    return (numAciertos*1.0)/(len(testset)*1.0)
    




# FOR DEBUGGING
"""
Borrar cuando se acabe
"""
def debug_print(s):
    if DEBUG:
        print s



if __name__ == "__main__":
    #--------------
    DEBUG=False
    #--------------

    k = 5
    trainset = read_file("iris.csv")
    debug_print(trainset)
    testset = read_file("iris_test.csv")
    debug_print(testset)
    result =  test( k, trainset, testset)
    
    print result

#    for idx in range(len(result)):
#        print result[idx],testset[idx][0:-1]

