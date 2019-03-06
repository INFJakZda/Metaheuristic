import numpy as numpy
import matplotlib.pyplot as plt

def loadInstance(fileName):
    with open(fileName) as fp:
        lines = fp.readlines()
    instance = [[int(nr) for nr in line.strip().split()] for line in lines]
    return instance

def draw(x, y):
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    fileName = "objects.data"

    #read data from file
    samples = loadInstance(fileName)
    
    #prepare coordinates data
    x_samples = [pair[0] for pair in samples]
    y_samples = [pair[1] for pair in samples]

    #draw sample plot
    draw(x_samples, y_samples)