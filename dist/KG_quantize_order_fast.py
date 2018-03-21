# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4,5]
qtype = ['Natural','Gray']

bmr = array([[ 0.03338   ,  0.03193   ],
       [ 0.04945   ,  0.032905  ],
       [ 0.07536667,  0.0433    ],
       [ 0.12259   ,  0.0653925 ],
       [ 0.188642  ,  0.104688  ]])
       
bgr = array([[ 1.,  1.],
       [ 2.,  2.],
       [ 3.,  3.],
       [ 4.,  4.],
       [ 5.,  5.]])
       
plt.figure(figsize=(8,5))
plt.plot(order,bmr[:,0],'ko-',label=qtype[0])
plt.plot(order,bmr[:,1],'k^:',label=qtype[1])
plt.ylim(0,0.2)
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