# -*- coding: utf-8 -*-

import sys
import os
import datetime
import matplotlib.pyplot as plt
from numpy import arange,zeros

sys.path.append('../')
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time = 1
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

''' 多组取平均 '''
gro_num = 100
mtype_num = len(mtype)
times = zeros(mtype_num)

''' 采样 '''
rssi_A, rssi_B, rssi_E  = sampling('RSSI', sampling_period,sampling_time)  
phase_A,phase_B,phase_E = sampling('Phase',sampling_period,sampling_time)

for i in range(mtype_num):
    
    print 'Running... Current group:',i
    begin = datetime.datetime.now()
    
    if mtype[i] == 'RSSI':
        for j in range(gro_num):
            ''' RSSI Only '''
            bits_A_rssi,drop_list_A = quantization_thre(rssi_A)
            bits_B_rssi,drop_list_B = quantization_thre(rssi_B)
            bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
            bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
        
    elif mtype[i] == 'Phase':
        for j in range(gro_num):
            ''' Phase Only '''
            bits_A_phase = quantization_even(phase_A)
            bits_B_phase = quantization_even(phase_B)
    
    else:
        for j in range(gro_num):
            ''' RSSI量化 '''
            bits_A_rssi,drop_list_A = quantization_thre(rssi_A)
            bits_B_rssi,drop_list_B = quantization_thre(rssi_B)
            bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
            bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
            
            ''' Phase量化 '''
            bits_A_phase = quantization_even(phase_A)
            bits_B_phase = quantization_even(phase_B)
            
            ''' 合并 '''
            bits_A = merge(bits_A_rssi,bits_A_phase,mtype[i])
            bits_B = merge(bits_B_rssi,bits_B_phase,mtype[i])
        
    end = datetime.datetime.now()
    # 转化成毫秒ms，并求每组样例的平均耗时。另Alice和Bob同时做量化，因此除2求每个人的耗时
    times[i] = (end-begin).total_seconds()*1000/gro_num/2

''' 画图 '''
labels = ['RSSI Only', 'Phase Only', 'Cross', 'AND', 'OR', 'XOR', 'Syn']
plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),times):
    plt.bar(x+1,times[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%d'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0,70)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('Time(ms)')
plt.title('Time of different merge method')
plt.show()

print 'Program Finished'