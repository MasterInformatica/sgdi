# -*- coding: utf-8 -*-
from mrjob.job import MRJob
import re
import os

class MRWordCount(MRJob):

  # Fase MAP (line es una cadena de texto)
  def mapper(self, key, line):
    data = re.sub('[^A-Za-z ]+', '', line).split()
    for w in data:
      if w != "":
        yield w.lower(), os.environ["map_input_file"]

  # Fase REDUCE (key es una cadena texto, values un generador de valores)
  def reducer(self, key, values):
    lib = {}
    mas = False
    for l in values:
      if l in lib:
        lib[l] = lib[l] + 1
        if lib[l] > 20:
          mas = True
      else:
        lib[l] = 1
    if mas:
      yield key, sorted(lib.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
  MRWordCount.run()
