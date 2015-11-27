# -*- coding: utf-8 -*-
import csv
from scipy.spatial import distance
import pprint


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
    pass


""" Devuleve una pareja "clistering, centroides", del estilo:
{0: [inst1, inst2, inst3],
 1: [inst4],
 2: [inst5] },

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


    # La estructura cluster [(centroide, [instancias]),
    #                        (centroide, [instancias]), ....
    # almacena por cada cluster, su centroide, y las instancias actuales.
    clustering = {}

    for i in range(k):
        clustering[i] =[]

    while(True):
        # 2.- Para cada instancia en C asignar al cluster con centroide
        # más cercano
        for i in instancias:
            dist_menor = float("inf")
            idx_menor = -1
            # calcular la distancia a todos los centroides c[k][0],
            # quedarse con la distancia menor (y el idx)
            for idx in range(k):
                d = distance.euclidean(i, centroides[idx])
                if d < dist_menor:
                    idx_menor = idx
                    dist_menor = d
            # añadimos la instancia actual al cluster provisional
            clustering[idx_menor].append(i)

        # 3.- Calcular los nuevos centroides de cada cluster
        # cluster,cambio = actualiza_centroides(clusters)
        nuevos_centroides = actualiza_centroides(clustering)
        if nuevos_centroides == centroides:
            # SALIR
            break
        else:
            centroides = nuevos_centroides

    return (clustering, centroides)


def actualiza_centroides(clustering):
    return [get_centroide(clustering[idx]) for idx in clustering] 


""" 
Dado una lista de instancias, devuleve su centroide
"""
def get_centroide(lista):
    centroide = lista[0]
    N = len(lista)
    M = len(centroide)
    for i in range(1,N):
        for j in range(M):
            centroide[j] += lista[i] [j]

    for i in range(M):
        centroide[i] /= N*1.0

    return centroide


"""
k-means(C:conjunto de datos, k:nat)

2.- Para cada instancia en C asignar al cluster con centroide 
      más cercano
3.- Calcular los nuevos centroides de cada cluster
4.- Repetir los pasos 2.- y 3.- hasta que las instancias dentro de cada 
      cluster no cambien
"""



if __name__ == "__main__":
    instancias = read_file()
    pp =  pprint.PrettyPrinter(indent=4)
    pp.pprint( kmeans(4, instancias, instancias[0:4]))
