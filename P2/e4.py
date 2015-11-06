# -*- coding: utf-8 -*-
from mrjob.job import MRJob
import re
import os

class MRWordCount(MRJob):

  # Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    w = line.split()
    error = (0,1)[int(w[-2]) >= 400 and int(w[-2]) < 600]

    yield w[0],[int((w[-1],0)[w[-1]=='-']),error]

  def combiner(self, key, values):
    total = 0
    size = 0
    n_errores = 0

    for v in values:
      total += 1
      size += v[0]
      n_errores += v[1]

    yield key,[total, size, n_errores]

  # Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    total = 0
    size = 0
    n_errores = 0

    for v in values:
      total += v[0]
      size += v[1]
      n_errores += v[2]

    yield key, [total, size, n_errores]



if __name__ == '__main__':
  MRWordCount.run()
