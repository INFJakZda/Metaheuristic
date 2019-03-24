import numpy as np
import time

from helpers import loadInstance, calculateTime, prepareMatrix
from algorithms import greedyMST_groups, greedMethod, regretMethod
from drawing import draw, drawRegret

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
    return bestGroup


if __name__ == '__main__':
    # fileName = "data/objects20_06.data"
    fileName = "data/objects.data"
    # fileName = "data/test.data"

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
    # regretGroups = greedMethod(original_matrix, original_samples)
    # print(calculateTime(regretGroups, original_samples))

    # VII TODO prepare tests
    #   - 100 tests for 2 methods
    #   - save best solution and its image with colored groups
    #   - calculate min, max, mean
    groups = testing(original_matrix, original_samples)
    drawRegret(x_samples, y_samples, groups)


    # draw sample plot
    # draw(x_samples, y_samples, Edges)
