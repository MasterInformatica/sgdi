# -*- coding: utf-8 -*-
"""
 Sistemas de gestion de datos y de la informacion 
 Practica 1
 Luis Maria Costero Valero 
 Jesus Javier Domenech Arellano 

 Nosotros, Luis M. Costero y Jesus Domenech, declaramos la autoria completa de este documento. 

"""


from mrjob.job import MRJob


class MRWordCount(MRJob):

  # Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    data = line.split('\t')
    if(float(data[2]) < 2 and data[4] != "--"):
      yield "triste", data[0]

  # Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    copia = list(values)
    yield len(copia), copia


if __name__ == '__main__':
    MRWordCount.run()
