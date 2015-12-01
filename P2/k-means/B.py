import matplotlib.pyplot as plt
from scipy.spatial import distance
import A


def plot(k,cohesion,tipe):
    eje_x = k
    eje_y = cohesion
    plt.plot(eje_x, eje_y)
    plt.ylabel('Coherencia '+tipe)
    plt.xlabel('K')
    plt.show()

def media(lista):
    return sum(lista)/len(lista)*1.0


def coherencia_diametro(cluster):
    dists = []
    N = len(cluster)
    for c in range(N):
        for i in range(c,N):
            dists.append(distance.euclidean(cluster[c],cluster[i]))
    return max(dists)


def coherencia_radio(cluster):
    c = A.get_centroide(cluster)
    return max([distance.euclidean(i,c) for i in cluster])

def coherencia_promedio(cluster):
    """
    SUM(dist(c,i)^2)/N
    """
    c = A.get_centroide(cluster)
    suma = 0
    for i in cluster:
        d = distance.euclidean(c,i)
        suma += d*d
    return suma/(len(cluster)*1.0)

if __name__ == "__main__":
    instancias = A.read_file()
    co_r = []
    co_d = []
    co_p = []
    K = range(2,21)
    for k in K:
        print "-------------",k,"-------------"
        res = A.kmeans(k, instancias)
        co_d.append(media([coherencia_diametro(res[0][c]) for c in res[0]]))
        co_r.append(media([coherencia_radio(res[0][c]) for c in res[0]]))
        co_p.append(media([coherencia_promedio(res[0][c]) for c in res[0]]))
    plot(K,co_d,"diametro")
    plot(K,co_r,"radio")
    plot(K,co_p,"promedio")
