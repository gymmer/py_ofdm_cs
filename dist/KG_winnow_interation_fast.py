# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

iteration = [0,1,2,3,4]

bmr = array([ 0.02327134,  0.00339609,  0.00019373,  0.        ,  0.        ])
bgr = array([ 0.53006667,  0.46356333,  0.40562667,  0.35352333,  0.30716   ])

plt.figure(figsize=(8,5))
plt.plot(iteration,bmr,'ko-')
plt.xlabel('Iteration')
plt.ylabel('BMR')
plt.title('BMR of different iteration')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr,'ko-',)
plt.xlabel('Iteration')
plt.ylabel('BGR')
plt.title('BGR of different iteration')
plt.show()