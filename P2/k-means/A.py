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


"""
Selecciona k centroides lo más alejado posible siguiendo el algoritmo:
...
...
"""
def select_initial_centroides(k, instancias):
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
        



""" Devuleve una pareja "clustering, centroides", del estilo,
donde el clustering es un diccionarios del estilo:
  {0: [inst1, inst2, inst3],
   1: [inst4],
   2: [inst5] },

y centroides es una lista de centroides.


Si la lista de centroides está vacia, se escogeran los centroides 
intentando que estén lo más alejados entre sí, con el siguiente algoritmo:
....
....
"""
def kmeans(k, instancias, centroides_ini = None):

    # 1.- elegir k puntos de C como centroides
    if(centroides_ini is None):
        centroides = select_initial_centroides(k, instancias)
    else:
        centroides = centroides_ini

    # centroides almacena una lista con los centroides en cada momento
    # clustering es un diccionario donde por cada cluster, aparencen las instancias clasificadas.
    clustering = {}

    while(True):
        # Cada iteracion vaciamos los clusters. 
        for i in range(k):
            clustering[i] =[]


        # 2.- Para cada instancia en C asignar al cluster con centroide
        # más cercano
        for i in instancias:
            idx = get_centroide_cercano(centroides, i)
            clustering[idx].append(i)


        # 3.- Calcular los nuevos centroides de cada cluster
        nuevos_centroides = actualiza_centroides(clustering)
        # Detectamos si ha habido cambios porque ha cambiado
        # algún centroide o no
        if nuevos_centroides == centroides:
            break  # SALIR
        else:
            centroides = nuevos_centroides
    # END WHILE

    return (clustering, centroides)



""" Dada una lista de centoides y una instancia,
devuelve el índice del centroide más cercano.
"""
def get_centroide_cercano(centroides, i):
    dist_menor = float("inf")
    idx_menor = -1

    for idx in range(len(centroides)):
        d = distance.euclidean(i, centroides[idx])
        if d < dist_menor:
            idx_menor = idx
            dist_menor = d

    return idx_menor


"""
Dado un diccionario de cluster - instancias de ese cluster,
devuleve una lista con los centroides de cada cluster
"""
def actualiza_centroides(clustering):
    return [get_centroide(clustering[idx]) for idx in clustering] 


""" 
Dado una lista de instancias, devuleve su centroide
"""
def get_centroide(lista):
    centroide = []
    N = len(lista)
    M = len(lista[0])

    for j in range(M):
        centroide.append(0)
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
    #    for i in result[0][r]:
    #        print "\t", i
