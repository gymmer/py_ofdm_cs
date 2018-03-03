# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import arange

times = [128.49, 41.56, 189.295, 172.245, 171.325, 169.465, 170.035]

labels = ['RSSI Only', 'Phase Only', 'Cross', 'AND', 'OR', 'XOR', 'Syn']
plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),times):
    plt.bar(x+1,times[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%d'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0,230)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('Time(ms)')
plt.title('Time of different merge method')
plt.show()