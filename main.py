import numpy as numpy
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

def loadInstance(fileName):
    with open(fileName) as fp:
        lines = fp.readlines()
    instance = [[int(nr) for nr in line.strip().split()] for line in lines]
    return instance

def prepareMatrix(samples):
    return euclidean_distances(samples, samples)

def draw(x, y):
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    fileName = "objects.data"
    # fileName = "test.data"

    # I read data from file
    samples = loadInstance(fileName)
    
    # II prepare coordinates data
    x_samples = [pair[0] for pair in samples]
    y_samples = [pair[1] for pair in samples]

    # III calculate matrix with euclidean distances
    matrix = prepareMatrix(samples)

    # IV 





    # draw sample plot
    # draw(x_samples, y_samples)
