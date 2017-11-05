# -*- coding: utf-8 -*-

import os
import numpy as np
from numpy import zeros,size,mean,arange,mod,pi
from function import BMR
from security_sampling import sampling
from security_quantize import quantization_thre,quantization_even,remain
from security_merge import merge
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

''' 采样参数 '''
sampling_period  = 1
sampling_time = 3

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 2
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or']

gro_num = 100
mtype_num = len(mtype)
bmr = zeros((gro_num,mtype_num))
bgr = zeros((gro_num,mtype_num))

for i in range(gro_num):
    for j in range(mtype_num):
        print 'Running... Current group: ',i,j
        
        ''' 采样 ''' 
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)  
        phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.9,0.4),2*pi)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_listA = quantization_thre(rssi_A,block_size,coef)
        bits_B_rssi,drop_listB = quantization_thre(rssi_B,block_size,coef)
        bits_A_rssi = remain(bits_A_rssi,drop_listA,drop_listB)
        bits_B_rssi = remain(bits_B_rssi,drop_listA,drop_listB)
        
        ''' Phase量化 '''
        bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
        bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
        
        ''' 合并 '''
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype[j])
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype[j])
        
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = size(bits_A)/(sampling_time*1000.0/sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

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