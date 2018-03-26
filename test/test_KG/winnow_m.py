# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.metric import BMR,BGR
from KG import sampling_RSSI,sampling_phase,quantize_phase,quantize_ASBG_1bit,remain,merge,winnow

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 20
mtype = 'cross'
iteration = 2
m = range(2,9)

''' 多组取平均 '''
group_num = 100
m_num     = len(m)
bmr = zeros((group_num,m_num))
bgr = zeros((group_num,m_num))

for i in range(group_num):
    for j in range(m_num):
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
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype)
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype)
        
        ''' 信息协调 '''
        bits_A,bits_B = winnow(bits_A,bits_B,iteration,m[j])
        
        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(m,bmr,'ko-')
plt.xlabel('m')
plt.ylabel('BMR')
plt.title('BMR of different m')
plt.show()

plt.figure(figsize=(8,5))
plt.plot(m,bgr,'ko-',)
plt.xlabel('m')
plt.ylabel('BGR')
plt.title('BGR of different m')
plt.show()

print 'Program Finished'