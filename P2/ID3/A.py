# -*- coding: utf-8 -*-

import csv
from sets import Set

"""
Function: read_file
Descr:
Input:
   filename: CSV File name to be read.
Return:
   List of instance for each file line.
"""
# -----------
DEBUG = True
# -----------

def read_file( filename = "car.csv" ):
    infile = open(filename,"r")
    reader = csv.reader(infile)
    inst = []
    attr = []
    key = []
    s = {}
    dic = {}
    clas = Set([])
    i = 0
    for row in reader:
        if DEBUG and i > 10:
            break
        if i == 0:
            j = 0
            for k in row[:-1]:
                s[k] = Set([])
                key.append(k)
                j += 1
        else:
            inst.append(row)
            j = 0
            for k in key:
                s[k].add(row[j])
                j += 1
            clas.add(row[-1])
        i += 1
    # to list
    clas = list(clas)
    i = 0
    for k in key:
        dic[k] = (i,list(s[k]))
        i += 1
    return (inst, dic, clas)

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
    (cp,allsameclass)=maxClass([i[-1] for i in inst])
    if allsameclass:
        return (cp,[])
    if len(candidates) == 0:
        return (cp,[])

    attr = selecciona_atributo(inst,candidates)
    nodo = (attr,[])
    setCand = set(candidates)
    setCand.remove(attr)
    newcandidates = list(setCand)   
    pos = attrib_dic[attr][0]
    for v in attrib_dic[attr][1]:
        C = particion(inst,pos,v)
        child = None
        if len(C) == 0:
            child = (cp,[],v)
        else:
            (A,B) = id3(C,attrib_dic,[],newcandidates)
            child = (A,B,v)
        nodo[1].append(child)
    return nodo

def particion(instances,attr_pos,value):
    return [i for i in instances if i[attr_pos] == value]

def selecciona_atributo(inst,candidates):
    return candidates[0]

def maxClass(classes):
    d = {}
    maxV = 0
    mC = ""
    for c in classes:
        if d.has_key(c):
            d[c] += 1
        else:
            d[c] = 0
        if d[c] > maxV:
            mC = c
            maxV = d[c]
    return (mC, maxV == len(classes))

def toDOT(Tree):
    dot = "digraph T {\n"
    n=0
    (d,n)= dotTree(Tree,n)
    dot+=d
    dot += "}"
    return dot
    
def dotTree(Tree,n):
    dot = ""
    m = n
    for child in Tree[1]:
        n+=1
        dot += "\t"+Tree[0]+str(m)+" -> "+child[0]+str(n)+' [label="'+child[2]+'"];\n'
        #        for c in child[1]:

        (d,n)= dotTree(child,n)
        dot += d
    return (dot,n)
if __name__ == '__main__' : 
    (inst,attr,clas) = read_file()
    candidates = [k for k in attr]
    ida = id3(inst,attr,clas,candidates)
    #    print ida
    #    print attr
    #    eof
    print toDOT(ida)
