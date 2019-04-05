import random
random.seed(0)

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

def initializeGroups(n = 20, size = 201):
    mylist = []
    for _ in range(0, n):
        x = random.randint(0, size - 1)
        mylist.append([x])
    return mylist

def prepareCheckList(points, size = 201):
    listofzeros = [-1] * size
    for idx, point in enumerate(points):
        listofzeros[int(point[0])] = idx
    return listofzeros

def prepareClosest(points, size = 201):
    listofinf = [999] * size
    for point in points:
        listofinf[int(point[0])] = 0
    return listofinf

def greedMethod(n, matrix, samples):
    samples_len = len(samples)
    
    # takes random 10 points
    groups = initializeGroups(n=n, size=samples_len)

    # prepare list of points and in which group point are
    listOfAvailablePoints = prepareCheckList(groups, size=samples_len)

    # prepare list of sublist where are sorted neighbours by length
    neighbours = [[] for _ in range(samples_len)]
    for idx in range(samples_len):
        neighbours[idx] = matrix[idx]
        neighbours[idx] = [(i, x) for i, x in enumerate(neighbours[idx])]
        neighbours[idx].sort(key=lambda tup: tup[1])
        neighbours[idx].pop(0)
    isElement = 1
    
    # add to groups another vertexes
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

def regretMethod(matrix, samples):
    samples_len = len(samples)
    # takes random 10 points
    groups = initializeGroups(size=samples_len)

    # prepare list of points and in which group point are
    listOfAvailablePoints = prepareCheckList(groups, size=samples_len)
    closestPoints = prepareClosest(groups, size=samples_len)

    # prepare list of sublist where are sorted neighbours by length
    neighbours = [[] for _ in range(samples_len)]
    for idx in range(samples_len):
        neighbours[idx] = matrix[idx]
        neighbours[idx] = [(i, x) for i, x in enumerate(neighbours[idx])]
        neighbours[idx].sort(key=lambda tup: tup[1])
        neighbours[idx].pop(0)
    isElement = 1
    
    # add to groups another vertexes
    while(isElement):
        minLength = 9999
        selectedElement = -1
        selectedGroup = -1
        toRemoveFromGroup = -1
        closestHelper = closestPoints.copy()
        availableHelper = listOfAvailablePoints.copy()
        for idxGroup, group in enumerate(groups):
            for ele in group:
                if minLength > neighbours[ele][0][1]:
                    if availableHelper[neighbours[ele][0][0]] == -1:
                        minLength = neighbours[ele][0][1]
                        selectedElement = neighbours[ele][0][0]
                        selectedGroup = idxGroup
                        toRemoveFromGroup = -1
                    else:
                        if neighbours[ele][0][1] < closestHelper[neighbours[ele][0][0]]:
                            toRemoveFromGroup = [availableHelper[neighbours[ele][0][0]], neighbours[ele][0][0]]
                            minLength = neighbours[ele][0][1]
                            selectedElement = neighbours[ele][0][0]
                            selectedGroup = idxGroup
                            closestHelper[neighbours[ele][0][0]] = neighbours[ele][0][1]
                            availableHelper[neighbours[ele][0][0]] = idxGroup

                        else:
                            neighbours[ele].pop(0)
        if toRemoveFromGroup != -1:
            if toRemoveFromGroup[1] in groups[toRemoveFromGroup[0]]: 
                groups[toRemoveFromGroup[0]].remove(toRemoveFromGroup[1])
        listOfAvailablePoints[selectedElement] = selectedGroup
        closestPoints[selectedElement] = minLength
        groups[selectedGroup].append(selectedElement)
        neighbours[selectedElement].pop(0)
        
        isElement = 0
        for ele in listOfAvailablePoints:
            if ele == -1:
                isElement = 1
    return groups
