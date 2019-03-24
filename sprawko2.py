from helpers import loadInstance, prepareMatrix, randomGroups
from algorithms import greedMethod
from drawing import drawRegret


if __name__ == '__main__':
    no_groups = 20

    # fileName = "data/objects20_06.data"
    fileName = "data/objects.data"
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
    print(random_groups)
    drawRegret(x_samples, y_samples, random_groups)

    # V Groups from first project - Greedy
    greed_groups = greedMethod(no_groups, matrix, samples)
    print(greed_groups)
    drawRegret(x_samples, y_samples, greed_groups)

    # VI TODO Local Search - Greedy 
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element which is closest to this ele
    
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
