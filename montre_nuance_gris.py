import matplotlib.pyplot as plt
import numpy as np
import sys

def graph (x) :
    f = open('donneesFormat/'+x+'.datV', 'r')
    lines = f.readlines()

# Enleve le \n qui reste.
    for i in range(len(lines)) :
        lines[i] = lines[i].rstrip('\n')

        plt.plot(lines)
        plt.show()

if __name__ == '__main__' :
    graph(sys.argv[1])
