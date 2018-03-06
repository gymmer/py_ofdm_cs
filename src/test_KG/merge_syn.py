# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,size,mean,mod,pi,hstack

sys.path.append('../')
from util.metric import BMR
from KG import sampling,quantization_even,quantization_thre,remain

os.system('cls')
plt.close('all')

def merge_syn(X,Y,w):
    '''字合成运算'''
    L = size(X)
    M = round(L*w)
    bits = hstack((Y[L-M:L], X[0:L-M]))
    return bits
    
''' 采样参数 '''
sampling_period = 1
sampling_time = 1

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 1
w = [i/10.0 for i in range(11)]

''' 多组取平均 '''
gro_num = 100
w_num = len(w)
bmr = zeros((gro_num,w_num))

for i in range(gro_num):
    for j in range(w_num):
        print 'Running... Current group: ',i,j
    
        ''' 采样 ''' 
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)  
        phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.9,0.4),2*pi)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
        bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
        bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
        bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
        
        ''' Phase量化 '''
        bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
        bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
        
        ''' 合并 '''
        L = min(size(bits_A_rssi),size(bits_A_phase))
        bits_A = merge_syn(bits_A_rssi[0:L],bits_A_phase[0:L],w[j])
        bits_B = merge_syn(bits_B_rssi[0:L],bits_B_phase[0:L],w[j])
        
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