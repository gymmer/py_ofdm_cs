# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array,arange

mtype = ['RSSI', 'Phase', 'cross', 'and', 'or']
mtype_num = len(mtype)

bmr = array([ 0.03109455,  0.03274833,  0.03140696,  0.0304668 ,  0.03187413])
bgr = array([ 0.26572333,  2.        ,  0.53198667,  0.2656    ,  0.26620667])

plt.figure(figsize=(8,5))
color = ['r','g','b','c','y']
for x,y in zip(arange(mtype_num),bmr):
    plt.bar(x+1,bmr[x],width=0.5,facecolor=color[x],edgecolor='white',label='%s'%(mtype[x]))
    plt.text(x+1+0.25,y,'%.4f'%y,ha='center',va='bottom')
plt.xlim(0.5,7.5)
plt.ylim(0.02,0.04)
plt.xticks([])
plt.xlabel('Merge method')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different merge method')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
color = ['r','g','b','c','y']
for x,y in zip(arange(mtype_num),bgr):
    plt.bar(x+1,bgr[x],width=0.5,facecolor=color[x],edgecolor='white',label='%s'%(mtype[x]))
    plt.text(x+1+0.25,y,'%.4f'%y,ha='center',va='bottom')
plt.xlim(0.5,7.5)
plt.ylim(0,2.5)
plt.xticks([])
plt.xlabel('Merge method')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different merge method')
plt.legend()
plt.show()