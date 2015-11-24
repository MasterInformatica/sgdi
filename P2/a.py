# -*- coding: utf-8 -*-
import csv
import pprint
from scipy.spatial import distance

"""
Function: toFloat
Input:
  string: string to be converted
Return:
  float or string if we can not convert
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
Input:
   filename: CSV File name to be read.
Return:
   List of instances for each file line.
"""
def read_file( filename = "iris_test.csv" ):
    infile = open(filename,"r")
    reader = csv.reader(infile)
    rows = []
    for row in reader:
        tmp = [toFloat(w) for w in row]
        rows.append(tmp)
    return rows[1:-1]



"""
Function: knn
Input:
   k: number of neighbours
   i: instance to be analiZ?????????????
   c: trainset
Return:
   a string who indicates the predicted class of i
"""
def knn ( k, i , c ):
    print "hi"

    # Nos quedamos con los k vecinos más cercanos. Las distancias las hacemos sin considerar la clas.e
    distancias = [distance.euclidean(i,v[1:-2]) for v in c]
    s = distancias.sort()#[1:k]   
    print s
    
    
        
"""
Function: test
Args:
   k: number of neighbours
   trainset: 
   testset:
Return:
->
"""
def test( k, trainset, testset):
    return "holi" #[knn(k,x,trainset)    for x in testset]

print "hi"
if __name__ == "__main__":
    k = 5
    #trainset = read_file("iris.csv")
    #testset = read_file("iris_test.csv")
    trainset = [[5.1, 3.5, 1.4, 0.2, 'Iris-setosa'], [4.9, 3.0, 1.4, 0.2, 'Iris-setosa'], [4.7, 3.2, 1.3, 0.2, 'Iris-setosa'], [4.6, 3.1, 1.5, 0.2, 'Iris-setosa'], [5.0, 3.6, 1.4, 0.2, 'Iris-setosa'], [5.4, 3.9, 1.7, 0.4, 'Iris-setosa'], [4.6, 3.4, 1.4, 0.3, 'Iris-setosa'], [5.0, 3.4, 1.5, 0.2, 'Iris-setosa'], [4.4, 2.9, 1.4, 0.2, 'Iris-setosa'], [4.9, 3.1, 1.5, 0.1, 'Iris-setosa'], [5.4, 3.7, 1.5, 0.2, 'Iris-setosa'], [4.8, 3.4, 1.6, 0.2, 'Iris-setosa'], [4.8, 3.0, 1.4, 0.1, 'Iris-setosa'], [4.3, 3.0, 1.1, 0.1, 'Iris-setosa'], [5.8, 4.0, 1.2, 0.2, 'Iris-setosa'], [5.7, 4.4, 1.5, 0.4, 'Iris-setosa'], [5.4, 3.9, 1.3, 0.4, 'Iris-setosa'], [5.7, 3.8, 1.7, 0.3, 'Iris-setosa'], [5.1, 3.8, 1.5, 0.3, 'Iris-setosa'], [5.4, 3.4, 1.7, 0.2, 'Iris-setosa'], [5.1, 3.7, 1.5, 0.4, 'Iris-setosa'], [4.6, 3.6, 1.0, 0.2, 'Iris-setosa'], [5.1, 3.3, 1.7, 0.5, 'Iris-setosa'], [4.8, 3.4, 1.9, 0.2, 'Iris-setosa'], [5.0, 3.0, 1.6, 0.2, 'Iris-setosa'], [5.0, 3.4, 1.6, 0.4, 'Iris-setosa'], [5.2, 3.5, 1.5, 0.2, 'Iris-setosa'], [5.2, 3.4, 1.4, 0.2, 'Iris-setosa'], [4.7, 3.2, 1.6, 0.2, 'Iris-setosa'], [4.8, 3.1, 1.6, 0.2, 'Iris-setosa'], [5.2, 4.1, 1.5, 0.1, 'Iris-setosa'], [5.5, 4.2, 1.4, 0.2, 'Iris-setosa'], [5.0, 3.2, 1.2, 0.2, 'Iris-setosa'], [5.5, 3.5, 1.3, 0.2, 'Iris-setosa'], [4.4, 3.0, 1.3, 0.2, 'Iris-setosa'], [5.1, 3.4, 1.5, 0.2, 'Iris-setosa'], [5.0, 3.5, 1.3, 0.3, 'Iris-setosa'], [4.5, 2.3, 1.3, 0.3, 'Iris-setosa'], [4.4, 3.2, 1.3, 0.2, 'Iris-setosa'], [5.0, 3.5, 1.6, 0.6, 'Iris-setosa'], [5.1, 3.8, 1.9, 0.4, 'Iris-setosa'], [4.8, 3.0, 1.4, 0.3, 'Iris-setosa'], [5.1, 3.8, 1.6, 0.2, 'Iris-setosa'], [4.6, 3.2, 1.4, 0.2, 'Iris-setosa'], [5.3, 3.7, 1.5, 0.2, 'Iris-setosa'], [5.0, 3.3, 1.4, 0.2, 'Iris-setosa']]
    testset = [[5.1, 3.5, 1.4, 0.3, 'Iris-setosa'], [5.4, 3.4, 1.5, 0.4, 'Iris-setosa'], [4.9, 3.1, 1.5, 0.1, 'Iris-setosa'], [4.9, 3.1, 1.5, 0.1, 'Iris-setosa'], [5.0, 2.0, 3.5, 1.0, 'Iris-versicolor'], [6.7, 3.1, 4.4, 1.4, 'Iris-versicolor'], [5.6, 2.7, 4.2, 1.3, 'Iris-versicolor'], [7.1, 3.0, 5.9, 2.1, 'Iris-virginica'], [7.6, 3.0, 6.6, 2.1, 'Iris-virginica'], [7.3, 2.9, 6.3, 1.8, 'Iris-virginica'], [6.4, 2.7, 5.3, 1.9, 'Iris-virginica'], [6.3, 2.7, 4.9, 1.8, 'Iris-virginica'], [7.9, 3.8, 6.4, 2.0, 'Iris-virginica'], [6.4, 2.8, 5.6, 2.2, 'Iris-virginica']]
    result =  test( k, trainset, testset)
    for idx in range(len(result)):
        print result[idx],testset[idx][0:-1]

