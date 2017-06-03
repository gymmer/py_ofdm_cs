# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:46:14 2016

@author: gymmer
"""

from pos_agreement import agreement
import matplotlib.pyplot as plt

def how_many_right(posA,posB):
    right = 0    
    for pos in posA:
        if pos in posB:
            right += 1
    return right
    
if __name__ == '__main__':
    P = 36
    group = 100
    iteration = [0,1,2,3,4]
    probability = []
    
    for i in range(len(iteration)):
        allright = 0.0
        for j in range(group):   
            print 'running group...',i,j
            posA,posB,posE = agreement(P,0.5,iteration[i])
            if how_many_right(posA,posB) == P:
                allright += 1
        probability.append(allright/group)
    
    plt.figure(figsize=(8,5))
    plt.plot(iteration,probability,'bo-')
    plt.xlabel('Iteration')
    plt.ylabel('Probability')
    plt.title('Probability of all pilots right')