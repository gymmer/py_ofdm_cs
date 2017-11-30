# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import arange

mtype = ['RSS Only', 'Phase Only', 'cross', 'and', 'or']
mtype_num = len(mtype)

times = [128.3905, 41.033, 184.0885, 166.836, 167.387]
color = ['lightgray','lightgray','lightgray','lightgray','lightgray']

plt.figure(figsize=(8,5))
for x,y in zip(arange(mtype_num),times):
    plt.bar(x+1,times[x],width=0.5,facecolor=color[x],edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%d'%(mtype[x],y),ha='center',va='bottom')
plt.xlim(0.5,6)
plt.ylim(0,230)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('Time(ms)')
plt.title('Time of different merge method')
plt.show()