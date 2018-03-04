# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = 25
coef = [i/10.0 for i in range(10)]

bmr = array([ 0.20455   ,  0.15849768,  0.12438839,  0.09430802,  0.06520508,
        0.0452854 ,  0.02478916,  0.01797577,  0.01391792,  0.00792872])

bgr = array([ 1.        ,  0.84210333,  0.71822667,  0.59553333,  0.51515333,
        0.43993333,  0.36399333,  0.30944   ,  0.26583   ,  0.21957667])

plt.figure(figsize=(8,5))
plt.plot(coef,bmr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('BMR')
plt.title('BMR of different coef(bl=%d)'%(block_size))
plt.show()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('BGR')
plt.title('BGR of different coef(bl=%d)'%(block_size))
plt.ylim(0,1)
plt.show()
