# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt

sys.path.append('../../src')
from util.function import how_many_equal
from KG import agreement

os.system('cls')
plt.close('all')

P = 36
group = 100
iteration = [0,1,2,3,4]
probability = []

for i in range(len(iteration)):
    allright = 0.0
    for j in range(group):   
        print 'Running... Current group: ',i,j
        posA,posB,posE = agreement(P,{'iteration': iteration[i]})
        if how_many_equal(posA,posB) == P:
            allright += 1
    probability.append(allright/group)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(iteration,probability,'ko-')
plt.xlabel('Iteration')
plt.ylabel('Probability')
plt.title('Probability of all pilots right')
plt.show()

print 'Program Finished'