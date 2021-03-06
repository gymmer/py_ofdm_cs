# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean,arange

sys.path.append('../../src')
from util.metric import BMR,BGR
from KG import sampling_RSSI,sampling_phase,quantize_phase,quantize_ASBG_1bit,remain,merge

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 1
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

''' 多组取平均 '''
group_num = 100
mtype_num = len(mtype)
bmr = zeros((group_num,mtype_num))
bgr = zeros((group_num,mtype_num))

for i in range(group_num):
    for j in range(mtype_num):
        print 'Running... Current group: ',i,j
        
        ''' 采样 ''' 
        rssi_A, rssi_B, rssi_E  = sampling_RSSI( sampling_period,sampling_time)  
        phase_A,phase_B,phase_E = sampling_phase(sampling_period,sampling_time)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_list_A = quantize_ASBG_1bit(rssi_A)
        bits_B_rssi,drop_list_B = quantize_ASBG_1bit(rssi_B)
        bits_A_rssi = remain(bits_A_rssi,drop_list_B)
        bits_B_rssi = remain(bits_B_rssi,drop_list_A)
        
        ''' Phase量化 '''
        bits_A_phase = quantize_phase(phase_A)
        bits_B_phase = quantize_phase(phase_B)
        
        ''' 合并 '''
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype[j])
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype[j])
        
        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
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

print 'Program Finished'