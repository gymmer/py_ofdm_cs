# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array,arange

mtype = ['RSS Only', 'Phase Only', 'cross', 'and', 'or']
mtype_num = len(mtype)

bmr = array([ 0.02936185,  0.03342333,  0.03184573,  0.0311136 ,  0.03218075])
bgr = array([ 0.26584667,  1.        ,  0.53119333,  0.26565667,  0.26675   ])

plt.figure(figsize=(8,5))
for x,y in zip(arange(mtype_num),bmr):
    plt.bar(x+1,bmr[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(mtype[x],y),ha='center',va='bottom')
plt.xlim(0.5,6)
plt.ylim(0.028,0.035)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('BMR')
plt.title('BMR of different merge method')
plt.show()

plt.figure(figsize=(8,5))
for x,y in zip(arange(mtype_num),bgr):
    plt.bar(x+1,bgr[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(mtype[x],y),ha='center',va='bottom')
plt.xlim(0.5,6)
plt.ylim(0,1.2)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('BGR')
plt.title('BGR of different merge method')
plt.show()