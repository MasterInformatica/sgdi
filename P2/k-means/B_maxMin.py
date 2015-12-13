# -*- coding: utf-8 -*-
"""
 Sistemas de gestion de datos y de la informacion 
 Practica 2
 Luis Maria Costero Valero 
 Jesus Javier Domenech Arellano 

 Nosotros, Luis M. Costero y Jesus Domenech, declaramos la autoria completa de este documento. 

"""

import matplotlib.pyplot as plt
from scipy.spatial import distance
import pylab
import A


def plot(k, coherencia, tipe):
    """
    Function: plot
    Descrp: Pinta la grafica de cohesion segun el k elegido
    Args:
    -> k: Lista de valores de k
    -> coherencia: Lista de la coherencia en orden con k
    -> tipe: Nombre de la coherencia aplicada
    Return:
    -> void
    """

    eje_x = k
    eje_y = coherencia
    plt.plot(eje_x, eje_y)
    plt.ylabel('Coherencia '+tipe)
    plt.xlabel('K')
    plt.show()

def media(lista):
    """
    Function: media
    Descrp: Calcula la media de la lista.
    Args:
    -> lista: Lista de la que calcular la media.
    Return:
    -> media de la lista
    """

    return sum(lista)/len(lista)*1.0


def coherencia_diametro(cluster):
    """
    Function: coherencia_diametro
    Descrp: Calcula la coherencia de un cluster por el
    metodo del diametro.
    Args:
    -> cluster: Lista de instancias que forman el cluster.
    Return:
    -> Valor de coherencia
    """
    
    dists = []
    N = len(cluster)
    for c in range(N):
        for i in range(c,N):
            dists.append(distance.euclidean(cluster[c],cluster[i]))
    # maximo de las distancias de todos a todos
    return max(dists)


def coherencia_radio(cluster):
    """
    Function: coherencia_radio
    Descrp: Calcula la coherencia de un cluster por el
    metodo del radio.
    Args:
    -> cluster: Lista de instancias que forman el cluster.
    Return:
    -> Valor de coherencia
    """

    c = A.get_centroide(cluster)
    # maximo de los radios (todas las instancias al centroide)
    return max([distance.euclidean(i,c) for i in cluster])


def coherencia_promedio(clustering):
    """
    Function: coherencia_promedio
    Descrp: Calcula la coherencia de un conjunto de clusters por la
    formula SUM(dist(c,i)^2)/N
    Args:
    -> clustering: Lista de clusters.
    Return:
    -> Valor de coherencia
    """


    suma = 0
    num = 0
    for clu in clustering:
        c = A.get_centroide(clustering[clu])
        for i in clustering[clu]:
            d = distance.euclidean(c,i)
            suma += d*d
            num +=1
    return suma/(num*1.0)

if __name__ == "__main__":
    instancias = A.read_file()
    co_r = []
    co_d = []
    co_p = []

    #Jugamos con los máximos y minimos
    r_max = []
    d_max = []
    r_min = []
    d_min = []

    K = range(2,21) # K = [2..20]

    for k in K:
        print "-------------",k,"-------------"
        res = A.kmeans(k, instancias)
        co_d.append(media([coherencia_diametro(res[0][c]) for c in res[0]]))
        co_r.append(media([coherencia_radio(res[0][c]) for c in res[0]]))
        co_p.append(coherencia_promedio(res[0]))

        d_max.append(max([coherencia_diametro(res[0][c]) for c in res[0]]))
        r_max.append(max([coherencia_radio(res[0][c]) for c in res[0]]))

        d_min.append(min([coherencia_diametro(res[0][c]) for c in res[0]]))
        r_min.append(min([coherencia_radio(res[0][c]) for c in res[0]]))


    # plot(K,co_d,"diametro")
    # plot(K,co_r,"radio")
    # plot(K,co_p,"promedio")





    fig, ax = plt.subplots()
    ax.plot(K, co_d, 'b-o', label='media')
    ax.plot(K, d_max, 'r-o', label='maximo')
    ax.plot(K, d_min, 'r-o', label='minimo')
    plt.ylabel('Coherencia diametro')
    plt.xlabel('K')
    ax.legend(loc='upper right')
    plt.show()


    fig, ax = plt.subplots()
    ax.plot(K, co_r, 'b-o', label='media')
    ax.plot(K, r_max, 'r-o', label='maximo')
    ax.plot(K, r_min, 'r-o', label='minimo')
    plt.ylabel('Coherencia radio')
    plt.xlabel('K')
    ax.legend(loc='upper right')
    plt.show()

    plot(K,co_p,"promedio")

