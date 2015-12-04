# -*- coding: utf-8 -*-

import csv
import math
from sets import Set

# ----------- si debug esta activo solo analiza 10 instancias
DEBUG = False
# -----------


"""
Function: read_file
Descr:
Input:
   filename: CSV File name to be read.
Return:
   List of instance for each file line.
"""
def read_file( filename = "lens.csv" ):
    infile = open(filename,"r")
    reader = csv.reader(infile)
    # variables que se van a devolver
    inst = [] # guarda todas las instancias
    dic = {} #
    clas = set([]) # guarda el nombre de todas las clases
    #                se convierte a lista al devolverlo
    key = [] # guarda los nombres de los atributos en orden
    s = {} # dicionario de sets para no repetir valores de atributos


    i = 0
    for row in reader:
        if DEBUG and i > 10:
            break
        if i == 0:
            # si es la primera fila cargamos el nombre de los atributos en orden
            # y preparamos el diccionario de sets
            for k in row[:-1]:
                s[k] = set([])
                key.append(k)
        else:
            # para cada instancia:
            # --la guardamos
            inst.append(row)
            # --guardamos en el dicionario de atributos su valor sin repetir
            for j in range(len(key)):
                # el valor no se repite por ser un set
                s[key[j]].add(row[j])
            # --guardamos el valor de la clase sin repetir para tener todas las clases posibles
            clas.add(row[-1])
        i += 1

    # vamos a convertir el diccionario de sets en el dicionario de listas tal como
    # pide el enunciado formando el par (posicion, [lista de valores])
    i = 0
    for k in key:
        dic[k] = (i,list(s[k]))
        i += 1

    return (inst, dic, list(clas))

def id3(inst, attrib_dic, classes, candidates):
    """
    tdidt(C:conjunto_datos, l:atributos_candidatos)
    cp := clase que aparece más veces en C
    si todas las instancias en C son de clase cj entonces
n        return new Hoja(cj);
    si l  es vacía entonces
        return new Hoja(cp);
    a := selecciona_atributo(C,l);
    n := new NodoInterno(a);
    para cada valor aj del atributo a
        Cj := particion(C,a,aj);      
        si Cj =  entonces n' := new Hoja(cp);
        si no n' := tdidt(Cj,l\{a});
        n.añadeHijo(n',aj);
    return n;
    Raiz = (Attr, [list of childs])
    NODO = (Attr, [list of childs],attr value)
    HOJA = (Clase,[],attr value)
    attr value es el valor del attr que ha llevado a ese nodo
    vamos que estan las etiquetas de los edge en los nodos
    """
    # calculamos a la misma vez la clase que mas se repite
    # y si todas las instancias tienen la misma clase
    (cp,allsameclass)=maxClass([i[-1] for i in inst])
    
    if allsameclass:
        # si todas tienen la misma clase
        # devolvemos una hoja (no tiene hijos) con el nombre de la clase
        return (cp,[])

    if len(candidates) == 0:
        # si no quedan atributos candidatos
        # devolvemos una hoja (no tiene hijos) con el nombre de la clase mas reptida
        return (cp,[])

    # elegimos el siguiente atributo por el cual se va a dividir el arbol
    attr = selecciona_atributo(inst,candidates,attrib_dic)

    # preparamos el nodo para este atributo
    nodo = (attr,[])
    # ##########################################################################
    # una manera fea de eliminar el elemento elegido sin complicarme la vida...#
    # OJO: mirar como quitar un elemento de una lista q no sabes donde esta    #
    # ##########################################################################
    setCand = set(candidates)
    setCand.remove(attr)
    newcandidates = list(setCand)   
    #############################################################################

    # obtenemos la posicion del atributo dentro de la lista de una instancia
    pos = attrib_dic[attr][0]

    for v in attrib_dic[attr][1]:
        # para cada posible valor del atributo elegido
        # --tomamos el subconjunto que tiene el valor v en ese atributo
        C = particion(inst,pos,v)

        child = None

        if len(C) == 0:
            # si el conjunto es vacio creamos una hoja
            # el tercer elemento del nodo es la etiqueta de la arista que lleva a ella
            child = (cp,[],v)
        else:
            # si no es vacio aplicamos id3 al conjunto
            (A,B) = id3(C,attrib_dic,[],newcandidates)
            # ###########################################################################
            # OJO: id3 devuelve el nodo raiz sin nombre para la arista que lleva a el   #
            # poque no existe dicha arista.. como se trata de un subarbol y si la tiene #
            # se la añadimos aqui.                                                      #
            # ###########################################################################
            child = (A,B,v)
        # añadimos el hijo al nodo actual por cada valor del atributo actual
        nodo[1].append(child)
    # el nodo es el elemento raiz del arbol (o subarbol)
    return nodo

def particion(instances,attr_pos,value):
    # devuelve el subconjunto de instancias cuyo atributo coincide con el valor pedido
    return [i for i in instances if i[attr_pos] == value]

def maxClass(classes):
    # contamos el numero de instancias que tienen cada clase
    # ademas devuelve si todas tienen la misma o no
    d = {}
    maxV = 0
    mC = ""
    for c in classes:
        if d.has_key(c):
            d[c] += 1
        else:
            d[c] = 1
        if d[c] > maxV:
            mC = c
            maxV = d[c]
    return (mC, maxV == len(classes))


# ###################################################
# El codigo de arriba es reutilizable para C4.5     #
# y para 5...(nuestro trabajo final en principio... #
# de aqui para abajo es la magia de ID3, eligiendo  #
# el atributo basandose en la entropia              #
# ###################################################


def selecciona_atributo(insts,candidates,attrib_dic):
    # Hay que seleccionar el que mayor ganancia nos da
    # return max([ganancia(insts,p) for p in candidates])
    
    # pero en realidad no devolvemos la ganacia sino 
    # la entropia si seleccionamos ese atributo
    # por lo que debemos coger el minimo
    minC = 1000
    v = 0
    for attr in candidates:
        attr_pos = attrib_dic[attr][0]
        aux = entropia_attr(insts,attr_pos)
        if(aux < minC):
            minC = aux
            v = attr
    return v


def entropia(insts):
    """
    Calcula la entropia de las instancias.
    """
    d = {}
    entropia = 0
    N = len(insts)*1.0
    # contamos el numero de veces que aparece cada clase
    for i in insts:
        if (d.has_key(i[-1])):
            d[i[-1]] += 1
        else:
            d[i[-1]]  = 1

    # Calculamos la entropia -sum(si/N * log2(si/N))
    for val in d:
        aux = d[val]/N
        entropia += aux * math.log(aux, 2)
        
    return -1.0*entropia

def entropia_attr(insts, attr_pos):
    """
    Calcula la entropia si seleccionamos un atributo
    """
    d = {}
    E_new = 0
    N = len(insts)*1.0
    # contamos el numero de veces que aparece cada valor
    for i in insts:
        if (d.has_key(i[attr_pos])):
            d[i[attr_pos]] += 1
        else:
            d[i[attr_pos]]  = 1

    # Calcula la suma total de entropia a partir de las entropias
    # paciales por la cantidad de veces que aparece
    # E_new = sum (si*E_i)/N
    for val in d:
        C = particion(insts,attr_pos,val) 
        E_new += d[val] * entropia(C)

    E_new = E_new / N

    # si quisieramos la ganancia
    # E_start = entropia(insts)
    # Ganancia = E_start - E_new
    # return E_start - E_new

    return E_new

if __name__ == '__main__' : 
    (inst,attr,clas) = read_file()
    candidates = [k for k in attr]
    print id3(inst,attr,clas,candidates)
    print clas

