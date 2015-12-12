# -*- coding: utf-8 -*-
"""
 Sistemas de gestion de datos y de la informacion 
 Practica 2
 Luis Maria Costero Valero 
 Jesus Javier Domenech Arellano 

 Nosotros, Luis M. Costero y Jesus Domenech, declaramos la autoria completa de este documento. 

"""

import csv
import copy
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


def read_file( filename = "customers.csv" ):
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


def select_initial_centroides(k, instancias):
    """
    Function: select_initial_centroides
    Descrp: Selecciona k centroides lo más alejados posible.
    Args:
    -> k: Numero de centroides a buscar
    -> instancias: Conjunto de instancias
    Return:
    -> Lista de los centroides.
    """

    c = [instancias[0]]
    while(k != 1):
        dist = []
        for i in instancias:
            dist.append((min([distance.euclidean(i,v) for v in c]),i))
        # ordenamos por el primer atributo y cojemos la 
        # instancia correspondiente al mas lejano
        cent = sorted(dist)[-1][1]
        c.append(cent)
        k -= 1
    return c
        

def kmeans(k, instancias, centroides_ini = None):
    """
    Function: kmeans
    Descrp: Devuelve una pareja (clustering, centroides),
    donde el clustering es un diccionario con el siguiente formato:
    {0: [inst1, inst2, inst3],
     1: [inst4],
     2: [inst5] },
    y centroides es una lista de centroides.
    Args:
    -> k: Numero de clusters a formar.
    -> instancias: Conjunto de instancias a clasificar
    -> centroides_ini: Conjunto de centroides de los clusters iniciales, puede ser vacío
    Return:
    -> Pareja (clustering, centroides)
    """
     
    # 1.- elegir k puntos de C como centroides
    if(centroides_ini is None or len(centroides_ini) < k):
        centroides = select_initial_centroides(k, instancias)
    else:
        centroides = centroides_ini

    # centroides almacena una lista con los centroides en cada momento
    # clustering es un diccionario donde por cada cluster, aparencen las instancias clasificadas.
    clustering = {}
    clustering2 = {}
    while(True):
        # Cada iteracion vaciamos la estructura de clusters. 
        for i in range(k):
            clustering2[i] = []

        # 2.- Para cada instancia en C asignar al cluster con centroide
        # más cercano
        for i in instancias:
            idx = get_centroide_cercano(centroides, i)
            clustering2[idx].append(i)

        # 3.- Calcular los nuevos centroides de cada cluster
        nuevos_centroides = actualiza_centroides(clustering2)

        # Detectamos si ha habido cambios porque ha cambiado
        # algún centroide o no
        if clustering == clustering2:
            break  # SALIR
        else:
            centroides = copy.deepcopy(nuevos_centroides)
            clustering = copy.deepcopy(clustering2)
    # END while

    return (clustering, centroides)


def get_centroide_cercano(centroides, i):
    """
    Function: get_centroide_cercano
    Descrp: Dada una lista de centoides y una instancia,
    devuelve el índice del centroide más cercano.
    Args:
    -> centroides: Lista de centroides.
    -> i: Instancia de referencia.
    Return:
    -> Indice del centroide mas cercano.
    """

    dist_menor = float("inf")
    idx_menor = -1
    for idx in range(len(centroides)):
        d = distance.euclidean(i, centroides[idx])
        if d < dist_menor:
            idx_menor = idx
            dist_menor = d

    return idx_menor


def actualiza_centroides(clustering):
    """
    Function: actualiza_centroides
    Descrp: Dado un diccionario de cluster - instancias de ese cluster,
    devuelve una lista con los centroides de cada cluster
    Args:
    -> clustering: Diccionario cluster - instancia.
    Return:
    -> Lista de los centroides de cada cluster.
    """

    return [get_centroide(clustering[idx]) for idx in clustering] 


def get_centroide(lista):
    """
    Function: get_centroide
    Descrp: Dada una lista de instancias, devuelve su centroide
    Args:
    -> lista: Instancias.
    Return:
    -> Centroide del conjunto de instancias.
    """

    centroide = []
    N = len(lista) # numero de instancias
    M = len(lista[0]) # tamaño de la instancia

    for j in range(M):
        centroide.append(0)
        # sumamos por coordenadas
        for i in range(N):
            centroide[j] += lista[i][j]
        centroide[j] /= N*1.0

    return centroide


if __name__ == "__main__":
    instancias = read_file()
    result = kmeans(4, instancias)
    for r in result[0]:
        print "cluster", r, "->", len(result[0][r]), "instancias"
        print "\tcent:", result[1][r]

