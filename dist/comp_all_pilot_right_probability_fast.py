# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 16:30:41 2017

@author: My402
"""

import matplotlib.pyplot as plt

iteration = [0,1,2,3,4]
probability= [
0.0,
0.24,
0.96,
0.99,
1.0]

plt.figure(figsize=(8,5))
plt.plot(iteration,probability,'ko-')
plt.xlabel('Iteration')
plt.ylabel('Probability')
plt.title('Probability of all pilots right')