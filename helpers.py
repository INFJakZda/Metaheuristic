import numpy as np
import random

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

def randomGroups(no_groups, sapmes_len):
    random_groups = [[] for i in range(no_groups)]
    vertex_idx = np.random.permutation(np.linspace(0, sapmes_len - 1, sapmes_len, dtype=np.int))
    for idx in vertex_idx:
        random_idx = random.randint(0, no_groups - 1)
        random_groups[random_idx].append(idx)
    return random_groups
