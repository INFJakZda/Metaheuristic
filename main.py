import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import time

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

def greedyMST_groups(matrix, n = 10):
    Edges = []
    min_lengths = []
    first = []
    for i in range(len(matrix[0])):
        min_lengths.append(matrix[0][i])
        first.append(0)
    
    for m in matrix:
        m[0] = 0

    for i in range(200):
        temp_min = min(filter(lambda x: x > 0, min_lengths))
        
        next_vertex = min_lengths.index(temp_min)
        last_vertex = first[next_vertex]
        min_lengths[next_vertex] = 0
        Edges.append([last_vertex, next_vertex, temp_min])
        for m in matrix:
            m[next_vertex] = 0
        for i in range(len(matrix[next_vertex])):
            if matrix[next_vertex][i] < min_lengths[i]:
                min_lengths[i] = matrix[next_vertex][i]
                first[i] = next_vertex
    
    result = 0
    
    for i in range(n-1):
        longest = [0, 0, 0]
        for edge in Edges:
            if longest[2] < edge[2]:
                longest = edge
        Edges.remove(longest)
    
    for edge in Edges:
        result += edge[2]
        
    return result, Edges
    
def draw(x, y, Edges):
    plt.scatter(x, y)
    for edge in Edges:
        plt.plot([x[edge[0]], x[edge[1]]], [y[edge[0]], y[edge[1]]], 'k-')
    plt.show()

def drawRegret(x, y, Edges):
    colors = cm.rainbow(np.linspace(0, 1, 10))
    for cl, group in enumerate(Edges):
        for ele in group:
            plt.scatter(x[ele], y[ele], color=colors[cl])
    plt.show()

def initializeGroups(n = 10, size = 201):
    mylist = []
    for _ in range(0, 10):
        x = random.randint(0, size - 1)
        mylist.append([x])
    return mylist

def prepareCheckList(points, size = 201):
    listofzeros = [-1] * size
    for idx, point in enumerate(points):
        listofzeros[int(point[0])] = idx
    return listofzeros

def regretMethod(matrix, samples):
    # takes random 10 points
    groups = initializeGroups()

    #prepare list of points and in which group point are
    listOfAvailablePoints = prepareCheckList(groups)

    # prepare list of sublist where are sorted neighbours by length
    neighbours = [[] for _ in range(201)]
    for idx in range(201):
        neighbours[idx] = matrix[idx]
        neighbours[idx] = [(i, x) for i, x in enumerate(neighbours[idx])]
        neighbours[idx].sort(key=lambda tup: tup[1])
        neighbours[idx].pop(0)
    isElement = 1
    while(isElement):
        minLength = 9999
        selectedElement = -1
        selectedGroup = -1
        for idxGroup, group in enumerate(groups):
            for ele in group:
                if minLength > neighbours[ele][0][1]:
                    if listOfAvailablePoints[neighbours[ele][0][0]] == -1:
                        minLength = neighbours[ele][0][1]
                        selectedElement = neighbours[ele][0][0]
                        selectedGroup = idxGroup
                    else:
                        neighbours[ele].pop(0)
        listOfAvailablePoints[selectedElement] = selectedGroup
        groups[selectedGroup].append(selectedElement)
        neighbours[selectedElement].pop(0)
        
        isElement = 0
        for ele in listOfAvailablePoints:
            if ele == -1:
                isElement = 1
        
    return groups

def calculateTime(groups, samples):
    totalTime = 0
    for group in groups:
        groupSamples = []
        for ele in group:
            groupSamples.append(samples[ele])
        groupMatrix = prepareMatrix(groupSamples)
        totalTime += calculateLengthMST(groupMatrix)
    return totalTime

def testing(original_matrix, original_samples):
    times = []
    results = []
    bestTime = np.inf
    bestGroup = 0
    for i in range(100):
        #print("START", i)
        start = time.time()
        regretGroups = regretMethod(original_matrix, original_samples)
        elapsedTime = time.time() - start
        times.append(elapsedTime)
        result = calculateTime(regretGroups, original_samples)
        results.append(result)
        if bestTime > result:
            bestTime = result
            bestGroup = regretGroups

    print('MIN:  ', np.min(results))
    print('MAX:  ', np.max(results))
    print('MEAN: ', np.average(results))
    print('STD:  ', np.std(results))
    print('TIME: ', np.mean(times))
    return regretGroups


if __name__ == '__main__':
    fileName = "objects.data"
    # fileName = "test.data"

    # I read data from file
    samples = loadInstance(fileName)
    original_samples = loadInstance(fileName)
    
    # II prepare coordinates data
    x_samples = [pair[0] for pair in samples]
    y_samples = [pair[1] for pair in samples]

    # III calculate matrix with euclidean distances
    matrix = prepareMatrix(samples)
    original_matrix = prepareMatrix(samples)

    # IV Prepare function to calculate MST
    # This function takes matrix and return length of minimum spanning tree
    #length = calculateLengthMST(matrix)

    # V TODO Greedy
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element which is closest to this ele
    
    # print(calculateLengthMST(matrix))
    # result_greedy, Edges_greedy = greedyMST_groups(matrix, 10)
    # print(result_greedy)
    # draw(x_samples, y_samples, Edges_greedy)

    # VI TODO Regret
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element with calculated regret
    # regretGroups = regretMethod(original_matrix, original_samples)
    # print(calculateTime(regretGroups, original_samples))

    # VII TODO prepare tests
    #   - 100 tests for 2 methods
    #   - save best solution and its image with colored groups
    #   - calculate min, max, mean
    groups = testing(original_matrix, original_samples)
    drawRegret(x_samples, y_samples, groups)


    # draw sample plot
    # draw(x_samples, y_samples, Edges)
