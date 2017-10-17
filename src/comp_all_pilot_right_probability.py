# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:46:14 2016

@author: gymmer
"""

from pos_agreement import agreement
from function import how_many_equal
import matplotlib.pyplot as plt
    
P = 36
group = 100
iteration = [0,1,2,3,4]
probability = []

for i in range(len(iteration)):
    allright = 0.0
    for j in range(group):   
        print 'running group...',i,j
        posA,posB,posE = agreement(P,0.5,iteration[i])
        if how_many_equal(posA,posB) == P:
            allright += 1
    probability.append(allright/group)

plt.figure(figsize=(8,5))
plt.plot(iteration,probability,'bo-')
plt.xlabel('Iteration')
plt.ylabel('Probability')
plt.title('Probability of all pilots right')