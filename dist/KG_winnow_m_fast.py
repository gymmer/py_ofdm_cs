# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

m = range(2,9)

bmr = array([ 0.        ,  0.0001127 ,  0.00143202,  0.00528637,  0.0177381 ,
        0.02582677,  0.0272549 ])

bgr = array([ 0.318  ,  0.42805,  0.4806 ,  0.50623,  0.46368,  0.381  ,  0.255  ])

plt.figure(figsize=(8,5))
plt.plot(m,bmr,'ko-')
plt.xlabel('m')
plt.ylabel('BMR')
plt.title('BMR of different m')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(m,bgr,'ko-',)
plt.xlabel('m')
plt.ylabel('BGR')
plt.title('BGR of different m')
plt.show()