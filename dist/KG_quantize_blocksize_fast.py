# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = range(5,41,5)
coef = 0.8

bmr = array([ 0.10690584,  0.04080994,  0.02137762,  0.01774302,  0.01482005,
        0.00998823,  0.00793783,  0.00525427])

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
