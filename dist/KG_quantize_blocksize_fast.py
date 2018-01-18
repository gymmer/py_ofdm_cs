# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = range(5,41,5)
coef = 0.8

bmr = array([ 0.12936534,  0.05939547,  0.04281098,  0.03430872,  0.02936504,
        0.02531191,  0.02266314,  0.01747585])

bgr = array([ 0.32092667,  0.2514    ,  0.24526333,  0.24496333,  0.26572667,
        0.25537667,  0.26142   ,  0.25875   ])

plt.figure(figsize=(8,5))
plt.plot(block_size,bmr,'ko-')
plt.xlabel('Block size')
plt.ylabel('BMR')
plt.title('BMR of different block sizes(coef=%.2f)'%coef)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(block_size,bgr,'ko-')
plt.xlabel('Block size')
plt.ylabel('BGR')
plt.title('BGR of different block sizes(coef=%.2f)'%coef)
plt.ylim(0,1)
plt.show()
