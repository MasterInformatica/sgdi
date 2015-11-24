import csv
import pprint
from scipy.spatial import distance

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
Args:
-> k: number of neighbours
-> i: instance to be analiZ?????????????
-> c: trainset
Return:
-> a string who indicates the predicted class of i
"""
def knn ( k, i , c ):
    pass

"""
Function: test
Args:
-> k: number of neighbours
-> trainset: 
-> testset:
Return:
->
"""
def test( k, trainset, testset):
    return [knn(k,x,trainset)    for x in testset]


if __name__ == "__main__":
    k = 5
    trainset = read_file("iris.csv")
    print trainset
    testset = read_file("iris_test.csv")
    print testset
    result =  test( k, trainset, testset)
    for idx in range(len(result)):
        print result[idx],testset[idx][0:-1]

