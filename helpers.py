import numpy as np

from sklearn.metrics.pairwise import euclidean_distances
from scipy.sparse.csgraph import minimum_spanning_tree

def loadInstance(fileName):
    with open(fileName) as fp:
        lines = fp.readlines()
    instance = [[int(nr) for nr in line.strip().split()] for line in lines]
    return instance

def prepareMatrix(samples):
    return euclidean_distances(samples, samples)

def calculateLengthMST(matrix):
    return np.sum(minimum_spanning_tree(matrix))

def calculateTime(groups, samples):
    totalTime = 0
    for group in groups:
        groupSamples = []
        for ele in group:
            groupSamples.append(samples[ele])
        groupMatrix = prepareMatrix(groupSamples)
        totalTime += calculateLengthMST(groupMatrix)
    return totalTime
