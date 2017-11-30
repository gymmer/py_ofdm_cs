# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = 25
coef = [i/10.0 for i in range(10)]

bmr = array([ 0.24451333,  0.20004815,  0.16102939,  0.12325057,  0.09725445,
        0.07626652,  0.0533309 ,  0.03958003,  0.03072994,  0.01884559])

bgr = array([ 1.        ,  0.84210333,  0.71822667,  0.59553333,  0.51515333,
        0.43993333,  0.36399333,  0.30944   ,  0.26583   ,  0.21957667])

plt.figure(figsize=(8,5))
plt.plot(coef,bmr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different coef(bl=%d)'%(block_size))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different coef(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)
