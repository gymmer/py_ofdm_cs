# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.metric import BMR,BGR
from KG import sampling_RSSI,quantize_ASBG_1bit,remain

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 1
block_size = range(5,41,5)
coef = 0.8

''' 多组取平均 '''
group_num = 100
block_num = len(block_size)
bmr = zeros((group_num,block_num))
bgr = zeros((group_num,block_num))

for i in range(group_num):
    for j in range(block_num):
        print 'Running... Current group: ',i,j
        
        ''' 采样 '''
        rssi_A,rssi_B,rssi_E = sampling_RSSI(sampling_period,sampling_time)

        ''' RSSI量化 '''
        bits_A,drop_list_A = quantize_ASBG_1bit(rssi_A,block_size[j],coef)
        bits_B,drop_list_B = quantize_ASBG_1bit(rssi_B,block_size[j],coef)
        bits_A = remain(bits_A,drop_list_B)
        bits_B = remain(bits_B,drop_list_A)
        
        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(block_size,bmr,'ko-')
plt.xlabel('Block size')
plt.ylabel('BMR')
plt.title('BMR of different block sizes(coef=%.2f)'%coef)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(block_size,bgr,'ko-')
plt.xlabel('Block size')
plt.ylabel('BGR')
plt.title('BGR of different block sizes(coef=%.2f)'%coef)
plt.ylim(0,1)
plt.show()

print 'Program Finished'
