# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,size,mean

sys.path.append('../')
from util.metric import BMR,BGR
from KG import sampling,quantization_thre,remain

os.system('cls')
plt.close('all')

''' 采样参数 '''
sampling_period = 1
sampling_time = 1

''' 量化参数 '''
block_size = range(5,41,5)
coef = 0.8

''' 多组取平均 '''
group_num = 100
block_num = size(block_size)
bmr = zeros((group_num,block_num))
bgr = zeros((group_num,block_num))

for i in range(group_num):
    for j in range(block_num):
        print 'Running... Current group: ',i,j
        
        ''' 采样 '''
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)

        ''' RSSI量化 '''
        bits_A,drop_list_A = quantization_thre(rssi_A,block_size[j],coef)
        bits_B,drop_list_B = quantization_thre(rssi_B,block_size[j],coef)
        bits_A = remain(bits_A,drop_list_A,drop_list_B)
        bits_B = remain(bits_B,drop_list_A,drop_list_B)
        
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
