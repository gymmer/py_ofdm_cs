# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../')
from util.metric import BMR
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time = 1
mtype = 'syn'
w = [i/10.0 for i in range(11)]

''' 多组取平均 '''
gro_num = 100
w_num = len(w)
bmr = zeros((gro_num,w_num))

for i in range(gro_num):
    for j in range(w_num):
        print 'Running... Current group: ',i,j
    
        ''' 采样 ''' 
        rssi_A, rssi_B, rssi_E  = sampling('RSSI', sampling_period,sampling_time)  
        phase_A,phase_B,phase_E = sampling('Phase',sampling_period,sampling_time)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_list_A = quantization_thre(rssi_A)
        bits_B_rssi,drop_list_B = quantization_thre(rssi_B)
        bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
        bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
        
        ''' Phase量化 '''
        bits_A_phase = quantization_even(phase_A)
        bits_B_phase = quantization_even(phase_B)
        
        ''' 合并 '''
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype,w[j])
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype,w[j])
        
        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)

bmr = mean(bmr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(w,bmr,'ko-')
plt.xlabel('w')
plt.ylabel('BMR')
plt.title('BMR of different w')
plt.show()

print 'Program Finished'