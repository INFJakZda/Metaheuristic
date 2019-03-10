import numpy as np
import matplotlib.pyplot as plt
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

def greedyMST(matrix):
    temp_matrix = matrix
    F = []
    Edges = []
    F.append((0, matrix[0]))
    
    for m in matrix:
        m[0] = 0
    
    for i in range(200):
        min_len = 0
        for f in F:
            vertex = list(f[1])
            temp_min = min(filter(lambda x: x > 0, vertex))
            if min_len == 0 or temp_min < min_len:
                min_len = temp_min
                next_vertex = vertex.index(min_len)
                last_vertex = f[0]
        F.append((next_vertex, matrix[next_vertex]))
        Edges.append([last_vertex, next_vertex, min_len])
        for m in matrix:
            m[next_vertex] = 0
    
    result = 0
    for edge in Edges:
        result += edge[2]
        
    return result
    
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

    # IV Prepare function to calculate MST
    # This function takes matrix and return length of minimum spanning tree
    #length = calculateLengthMST(matrix)

    # V TODO Greedy
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element which is closest to this ele
    
    print(calculateLengthMST(matrix))
    print(greedyMST(matrix))
    

    # VI TODO Regret
    #   - Divide matrix on 10 groups
    #   - In every group is one element
    #   - Add to every ggroup element with calculated regret

    # VII TODO prepare tests
    #   - 100 tests for 2 methods
    #   - save best solution and its image with colored groups
    #   - calculate min, max, mean



    # draw sample plot
    # draw(x_samples, y_samples)
