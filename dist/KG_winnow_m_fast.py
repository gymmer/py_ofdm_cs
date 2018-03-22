# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

m = range(2,9)

bmr = array([  1.03851790e-05,   1.52936703e-04,   1.39424211e-03,
         7.31063179e-03,   2.20290503e-02,   3.15397842e-02,
         3.47667963e-02])

bgr = array([ 0.2863035,  0.389466 ,  0.4458   ,  0.4770125,  0.4906125,
        0.4952365,  0.4974325])

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