# -*- coding: utf-8 -*-

import A


def toDOT(Tree):
    # esta funcion inicializa la construccion del dot
    # y configura su construccion
    dot = "digraph T {\n"
    n=0
    (d,n)= dotTree(Tree,n)
    dot+=d
    dot += "}"
    return dot
    
def dotNodo(Nodo,n):
    # escribe el nodo y manda escribir sus hijos...
    # como el arbol va a tener nodos con el mismo nombre
    # el atributo n nos asegura que cada nodo sera unico
    dot = ""
    m = n # n tiene que ser el mismo para todos los hijos por eso lo guardamos en m
    for child in Nodo[1]:
        # escribimos cada arista con los hijos e incrementamos n para evitar repeticiones
        # dado que puede repetirse el nombre en los hijos
        n+=1
        # ######## Nombre del Nodo ->   Nombre de su hijo  [ valor del atributo que divide]
        dot += "\t"+Nodo[0]+str(m)+" -> "+child[0]+str(n)+' [label="'+child[2]+'"];\n'
        if len(child[1]) == 0:
            # es una hoja y por tanto una clase le damos un aspecto diferente
            # ademas no mandamos escribir sus hijos
            dot += "\t"+child[0]+str(n)+ '[];\n'
        else:
            # si no es una hoja lo pintamos
            (d,n)= dotNodo(child,n)
            dot += d
    return (dot,n)


if __name__ == '__main__' : 
    (inst,attr,clas) = A.read_file()
    candidates = [k for k in attr]
    ida = A.id3(inst,attr,clas,candidates)
    print toDOT(ida)
