# -*- coding: utf-8 -*-

import csv
import pprint
from scipy.spatial import distance


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


def knn ( k, i , c ):
    """
    Function: knn
    Descr: Calcula la clase recomendada para la instancia a analizar
    Input:
    -> k: Numero de vecinos a tener en cuenta 
    -> i: Instancia a analizar
    -> c: Conjunto de entrenamiento
    Return:
    -> Clase recomendada para la instancia.
    """

    clases = clase_kvecinos_cercanos(k,i,c)
    return mode(clases)


def clase_kvecinos_cercanos(k, i, c):
    """
    Function: clase_kvecinos_cercanos
    Descrp: Devuelve las k clases de los k vecinos más cercanos 
    Args:
    -> k: Numero de vecinos a tener en cuenta 
    -> i: Instancia a analizar
    -> c: Conjunto de entrenamiento
    Return:
    -> Lista de clases de los k vecinos
    """

    # si tienen el mismo tamaño significa que i tiene la clase incorporada
    if len(i) == len(c[0]):
        distances = [ distance.euclidean(i[:-1],v[:-1]) for v in c]
    else:
        distances = [ distance.euclidean(i,v[:-1]) for v in c]

    # creamos las parejas (distancia, clase)
    par = []
    for i in range(0,len(c)):
        par += [(distances[i], c[i][-1])]
    
    # nos quedamos con las k instancias con distancia menor
    par = sorted(par)[:k]
    # y solamente con la clase, sin las distancias
    par = [p[1] for p in par]

    return par
    

def mode(lista):
    """
    Function: media
    Descrp: Calcula la moda de la lista.
    Args:
    -> lista: Lista de la que calcular la moda.
    Return:
    -> moda de la lista
    """

    max_num = -1
    moda = None
    dic={}

    for p in lista:
        if not p in dic:
            dic[p] = 1
        else:
            dic[p] += 1
        if max_num < dic[p]:
            max_num = dic[p]
            moda = p

    return moda


def test( k, trainset, testset):
    """
    Function: test
    Descr: Ejecuta knn para las instancias del testset y comprueba el
    porcentaje de acierto
    Input:
    -> k: number of neighbours
    -> trainset: Conjunto de entrenamiento
    -> testset: Conjunto de instancias a predecir
    Return:
    -> Porcentaje de acierto
    """

    clasificacion = [knn(k,x,trainset)    for x in testset]
    numAciertos = 0

    for i in range(0, len(testset)):
        print clasificacion[i] ,",", testset[i][-1]
        if clasificacion[i] == testset[i][-1]:
            numAciertos += 1

    return (numAciertos*1.0)/(len(testset)*1.0)

    
if __name__ == "__main__":
    k = 5
    trainset = read_file("iris.csv")
    testset = read_file("iris_test.csv")
    result =  test( k, trainset, testset)
    
    print result
    # for idx in range(len(result)):
    #     print result[idx],testset[idx][0:-1]

