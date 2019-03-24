from helpers import loadInstance, prepareMatrix, randomGroups
from algorithms import greedMethod
from drawing import drawRegret

def count_result(groups, matrix):
    sum_all = 0
    count_pairs = 0
    for group in groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                sum_all += matrix[group[i]][group[j]]
        count_pairs += sum(range(len(group)))
    return sum_all / count_pairs, sum_all, count_pairs

def delta(old_groups, element, matrix, old_sum_all, old_count_pairs): #element - [id, stara grupa, nowa grupa]
    sum_amplitude = 0
    pairs_amplitude = 0
    for edge in old_groups[element[1]]:
        sum_amplitude -= matrix[element[0]][edge]
    for edge in old_groups[element[2]]:
        sum_amplitude += matrix[element[0]][edge]
    pairs_amplitude -= sum(range(len(old_groups[element[1]]))) + sum(range(len(old_groups[element[2]])))
    pairs_amplitude += sum(range(len(old_groups[element[1]]) - 1)) + sum(range(len(old_groups[element[2]]) + 1))
    #print(sum_amplitude, pairs_amplitude)
    new_sum_all = old_sum_all + sum_amplitude
    new_count_pairs = old_count_pairs + pairs_amplitude
    if new_count_pairs != 0:
        print("OK")
        return new_sum_all / new_count_pairs, new_sum_all, new_count_pairs
    else:
        print("Error")
        return 0, 0, 0


def get_neighbours_from_other_groups(group, matrix, niegh_dist):    #returns dict with {ele: [(element_index, distance), ...]} for every ele from this group
    neighbours = dict((ele, []) for ele in group)
    for idx in group:
        neighbours[idx] = matrix[idx]
        neighbours[idx] = [(i, x) for i, x in enumerate(neighbours[idx]) if i not in group and x < niegh_dist]
        neighbours[idx].sort(key=lambda tup: tup[1])
        #neighbours[idx].pop(0)
    return neighbours

def checkGroup(ele, groups):
    for idx, group in enumerate(groups):
        if ele in group:
            return idx

def greedySearch(groups, matrix, niegh_dist, sum_all, count_pairs, result):
    for group_idx, group in enumerate(groups):
        neighbours = get_neighbours_from_other_groups(group, matrix, niegh_dist)
        #stop = 1
        #while(stop):
            #stop_while = 1
        for key, array in neighbours.items():
            if array:
                #stop_while = 0
                for ele in array:
                    #new_sum = delta(greed_groups,[greed_groups[2][0], 2, 5], matrix, sum_all, count_pairs)
                    new_group = checkGroup(ele[0], groups)
                    new_result, new_sum_all, new_count = delta(groups, [ele[0], group_idx, new_group], matrix, sum_all, count_pairs)
                    if new_result < result:
                        #TODO
                        #print(ele)
                        groups[group_idx].append(ele[0])
                        groups[new_group].remove(ele[0])
                        result = new_result
                        sum_all = new_sum_all
                        count_pairs = new_count
                neighbours[key] = []
            # if stop_while == 1:
            #     stop = 0
    return groups

if __name__ == '__main__':
    no_groups = 20
    niegh_dist = 30

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

    # IV Random Groups
    random_groups = randomGroups(no_groups, len(samples))
    # print(random_groups)
    # drawRegret(x_samples, y_samples, random_groups)

    # V Groups from first project - Greedy
    greed_groups = greedMethod(no_groups, matrix, samples)
    # print(greed_groups)
    # drawRegret(x_samples, y_samples, greed_groups)

    # VI TODO Local Search - Greedy 
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element which is closest to this ele
    result, sum_all, count_pairs = count_result(random_groups, matrix)
    drawRegret(x_samples, y_samples, random_groups)
    print(result, sum_all)
    groups = greedySearch(random_groups, matrix, niegh_dist, sum_all, count_pairs, result)
    results, sumall, count_pairss = count_result(groups, matrix)
    print(results, sumall)
    drawRegret(x_samples, y_samples, groups)
    
    # VII TODO Local Search - Steep
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element with calculated regret
    # regretGroups = greedMethod(original_matrix, original_samples)
    # print(calculateTime(regretGroups, original_samples))

    # VIII TODO prepare tests
    #   - 100 tests for 4 methods
    #   - save best solution and its image with colored groups
    #   - calculate min, max, mean

    # print(count_result(random_groups, matrix))
    # result, sum_all, count_pairs = count_result(greed_groups, matrix)
    # print(result, sum_all, count_pairs)
    # print(delta(greed_groups,[greed_groups[2][0], 2, 5], matrix, sum_all, count_pairs))
