# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,size,arange,mod,pi

sys.path.append('../')
from util.metric import UST
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')

''' 采样参数 '''
sampling_period = 1
sampling_time = 20

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 1
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

mtype_num = len(mtype)
ust = zeros(mtype_num)

''' 采样 ''' 
rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.8,0.4)  
phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.8,0.4),2*pi)
    
''' RSSI量化 '''
bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)

''' Phase量化 '''
bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)

''' 合并 '''
bits_A_cross = merge(bits_A_rssi,bits_A_phase,'cross')
bits_A_and = merge(bits_A_rssi,bits_A_phase,'and')
bits_A_or = merge(bits_A_rssi,bits_A_phase,'or')
bits_A_xor = merge(bits_A_rssi,bits_A_phase,'xor')
bits_A_syn = merge(bits_A_rssi,bits_A_phase,'syn')

''' 评价性能 '''
ust[0] = UST(bits_A_rssi)
ust[1] = UST(bits_A_phase)
ust[2] = UST(bits_A_cross)
ust[3] = UST(bits_A_and)
ust[4] = UST(bits_A_or)
ust[5] = UST(bits_A_xor)
ust[6] = UST(bits_A_syn)
    
''' 画图 '''
labels = ['RSSI Only', 'Phase Only', 'Cross', 'AND', 'OR', 'XOR', 'Syn']
plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),ust):
    plt.bar(x+1,ust[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0,1)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('P_value')
plt.title('Universal Statistical Test of different merge method')
plt.show()

print 'Program Finished'