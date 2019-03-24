import numpy as np
import matplotlib.pyplot as plt    
import matplotlib.cm as cm

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
