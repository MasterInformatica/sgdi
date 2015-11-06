# -*- coding: utf-8 -*-
from mrjob.job import MRJob


class MRWordCount(MRJob):

  # Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    data = line.split(',')
    yield data[2], float(data[8])

  # Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    copia = list(values)
    yield key, (min(copia),max(copia))


if __name__ == '__main__':
    MRWordCount.run()
