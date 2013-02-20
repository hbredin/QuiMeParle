import matplotlib.pyplot as plt
import numpy as np
import sys


f = open('donneesFormat/'+sys.argv[1]+'.datV')
lines = f.readlines()

# Enleve le \n qui reste.
for i in range(len(lines)) :
    lines[i] = lines[i].rstrip('\n')

plt.plot(lines)
plt.show()

