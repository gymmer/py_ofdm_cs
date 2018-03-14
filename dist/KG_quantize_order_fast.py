# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4]
qtype = ['Natural','Gray']

bmr = array([[ 0.03262   ,  0.03237   ],
       [ 0.04919   ,  0.03219   ],
       [ 0.07549333,  0.04400667],
       [ 0.12286   ,  0.06627   ]])
       
bgr = array([[ 1.,  1.],
       [ 2.,  2.],
       [ 3.,  3.],
       [ 4.,  4.]])
       
plt.figure(figsize=(8,5))
plt.plot(order,bmr[:,0],'k.-',label=qtype[0])
plt.plot(order,bmr[:,1],'k^:',label=qtype[1])
plt.ylim(0,0.14)
plt.xlabel('Quantize Order')
plt.ylabel('BMR')
plt.title('BMR of different order')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(order,bgr[:,0],'k.-',label=qtype[0])
plt.plot(order,bgr[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BGR')
plt.title('BGR of different order')
plt.legend()
plt.show()