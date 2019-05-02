import numpy as np
import time
import random

from helpers import loadInstance, prepareMatrix, randomGroups
from algorithms import greedMethod
from drawing import drawRegret


# ************ HELPERS FUNCTIONS ************
def count_result(groups, matrix):
    sum_all = 0
    count_pairs = 0
    for group in groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                sum_all += matrix[group[i]][group[j]]
        count_pairs += sum(range(len(group)))
    return sum_all / count_pairs, sum_all, count_pairs


def delta_cashe(old_groups, element, matrix, old_sum_all, old_count_pairs): #element - [id, stara grupa, nowa grupa]
    sum_amplitude = 0
    pairs_amplitude = 0
    for edge in old_groups[element[1]]:
        sum_amplitude -= matrix[element[0]][edge]
    for edge in old_groups[element[2]]:
        sum_amplitude += matrix[element[0]][edge]
    pairs_amplitude -= sum(range(len(old_groups[element[1]]))) + sum(range(len(old_groups[element[2]])))
    pairs_amplitude += sum(range(len(old_groups[element[1]]) - 1)) + sum(range(len(old_groups[element[2]]) + 1))
    #print(sum_amplitude, pairs_amplitude)
    return (old_sum_all + sum_amplitude) / (old_count_pairs + pairs_amplitude)

def checkGroup(ele, groups):
    for idx, group in enumerate(groups):
        if ele in group:
            return idx

def get_neighbours_from_other_groups(group, matrix, niegh_dist):    #returns dict with {ele: [(element_index, distance), ...]} for every ele from this group
    neighbours = dict((ele, []) for ele in group)
    for idx in group:
        neighbours[idx] = matrix[idx]
        neighbours[idx] = [(i, x) for i, x in enumerate(neighbours[idx]) if i not in group and x < niegh_dist]
        neighbours[idx].sort(key=lambda tup: tup[1])
        #neighbours[idx].pop(0)
    return neighbours


# ************ LOCAL SEARCH METHOD ************
def steepest_cashe_and_list(groups_original, matrix, neigh=35):
    groups = groups_original.copy()
    neighbours_all_groups = []
    for group in groups:
        neighbours_all_groups.append(get_neighbours_from_other_groups(group, matrix, neigh))
    for i in range(10000):
        #print(i)
        element = [0, 0, 0]
        result, sum_all, count_pairs = count_result(groups, matrix)
        minimal = result
        
        for j in range(len(neighbours_all_groups)):
            for idx, edge in enumerate(neighbours_all_groups[j]):
                for value in neighbours_all_groups[j][edge]:
                    group_idx = checkGroup(value[0], groups)
                    current = delta_cashe(groups, [edge, j, group_idx], matrix, sum_all, count_pairs)
                    if(current < minimal):
                        minimal = current
                        element = [edge, group_idx, j]
                        #print(element)
    
        #print(minimal)
        if (element == [0,0,0]):
            break
        else:
            groups[element[2]].remove(element[0])
            groups[element[1]].append(element[0])
            #print(element)
            #print(neighbours_all_groups[element[2]][element[0]])
            del neighbours_all_groups[element[2]][element[0]]
            neighbours_all_groups[element[1]] = get_neighbours_from_other_groups(groups[element[1]], matrix, neigh)
        element = [0,0,0]
        result = minimal
    return groups

def perturbate(groups, num):
    #TODO
    return groups

# ************ ITERATIVE LS ************
def testingILS(original_matrix, original_samples):
    bestResult = np.inf
    bestTime = 0
    bestGroup = []
    startGroup = []
    regretGroups = []
    random_groups = []

    random_groups = greedMethod(20, original_matrix, original_samples)
    regretGroups = steepest_cashe_and_list(random_groups, original_matrix)
    for i in range(1000):
        print("START", i)
        start = time.time()
        random_groups = perturbate(regretGroups, 10)
        regretGroups = steepest_cashe_and_list(random_groups, original_matrix)
        elapsedTime = time.time() - start
        print(str(elapsedTime) + " sec")
        result, _, _ = count_result(regretGroups, original_matrix)
        print(str(result) + " result")
        if bestResult > result:
            bestResult = result
            bestTime = elapsedTime
            bestGroup = regretGroups.copy()
            startGroup = random_groups.copy()
    print("BEST")
    print(bestTime)
    print(bestResult)
    print("BEST")

    return bestGroup, startGroup

# ************ MULTIPLE START LS ************
def testingMSLS(original_matrix, original_samples):
    best_times = []
    best_groups = []
    best_results = []
    
    for j in range(10):
        bestResult = np.inf
        bestTime = 0
        bestGroup = []
        startGroup = []
        regretGroups = []
        random_groups = []
        for i in range(100):
            print("START", j, i)
            random_groups = greedMethod(20, original_matrix, original_samples)
            start = time.time()
            regretGroups = steepest_cashe_and_list(random_groups, original_matrix)
            elapsedTime = time.time() - start
            print(str(elapsedTime) + " sec")
            result, _, _ = count_result(regretGroups, original_matrix)
            print(str(result) + " result")
            if bestResult > result:
                bestResult = result
                bestTime = elapsedTime
                bestGroup = regretGroups.copy()
                startGroup = random_groups.copy()
        print("BEST")
        print(bestTime)
        print(bestResult)
        print("BEST")
        best_times.append(bestTime)
        best_groups.append(bestGroup.copy())
        best_results.append(bestResult)

    print("***RESULTS***")
    print('MIN:  ', np.min(best_results))
    print('MAX:  ', np.max(best_results))
    print('MEAN: ', np.average(best_results))
    print('STD:  ', np.std(best_results))
    print("***TIME***")
    print('MIN: ', np.min(best_times))
    print('MAX: ', np.max(best_times))
    print('MEAN: ', np.average(best_times))
    print('STD:  ', np.std(best_times))   
    return bestGroup, startGroup


if __name__ == '__main__':
    no_groups = 20

    fileName = "data/objects20_06.data"
    # fileName = "data/objects.data"
    # fileName = "data/test.data"

    # I read data from file
    samples = loadInstance(fileName)
    
    # II prepare coordinates data
    x_samples = [pair[0] for pair in samples]
    y_samples = [pair[1] for pair in samples]

    # III calculate matrix with euclidean distances
    matrix = prepareMatrix(samples)

    # IV Groups from first project - Greedy
    greed_groups = greedMethod(no_groups, matrix, samples)
    print(count_result(greed_groups, matrix))
    #drawRegret(x_samples, y_samples, greed_groups)

    # V Start local search - steepest
    # steepest_groups = steepest(greed_groups, matrix)
    # drawRegret(x_samples, y_samples, steepest_groups)
    # print(count_result(steepest_groups, matrix))
    
    # TESTING MSLS
    best, random = testingILS(matrix, samples)
    drawRegret(x_samples, y_samples, random)
    drawRegret(x_samples, y_samples, best)
