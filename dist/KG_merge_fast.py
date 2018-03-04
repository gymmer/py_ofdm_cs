# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array,arange

bmr = array([ 0.01504646,  0.03356   ,  0.02444693,  0.02473701,  0.02353551, 0.04770955,  0.02345674])
bgr = array([ 0.26584667,  1.        ,  0.53119333,  0.26565667,  0.26675   ,  0.26499  ,  0.26546333])

labels = ['RSSI Only', 'Phase Only', 'Cross', 'AND', 'OR', 'XOR', 'Syn']
plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),bmr):
    plt.bar(x+1,bmr[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0.0,0.07)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('BMR')
plt.title('BMR of different merge method')
plt.show()

plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),bgr):
    plt.bar(x+1,bgr[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0,1.2)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('BGR')
plt.title('BGR of different merge method')
plt.show()