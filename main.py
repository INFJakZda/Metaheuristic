def loadInstance(fileName):
    with open(fileName) as fp:
        lines = fp.readlines()
    instance = [[int(nr) for nr in line.strip().split()] for line in lines]
    return instance



if __name__ == '__main__':
    fileName = "objects.data"

    samples = loadInstance(fileName)
    print(samples)