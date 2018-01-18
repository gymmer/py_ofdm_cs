# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4]
qtype = ['natural','gray']

bmr = array([[ 0.03303   ,  0.03282667],
       [ 0.04917667,  0.03266667],
       [ 0.07568778,  0.04364   ],
       [ 0.12215083,  0.06539167]])
       
bgr = array([[ 1.,  1.],
       [ 2.,  2.],
       [ 3.,  3.],
       [ 4.,  4.]])
       
plt.figure(figsize=(8,5))
plt.plot(order,bmr[:,0],'ko-',label=qtype[0])
plt.plot(order,bmr[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BMR')
plt.title('BMR of different order')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(order,bgr[:,0],'ko-',label=qtype[0])
plt.plot(order,bgr[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BGR')
plt.title('BGR of different order')
plt.legend()
plt.show()