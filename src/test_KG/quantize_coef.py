# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../')
from util.metric import BMR,BGR
from KG import sampling,quantize_ASBG_1bit,remain

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 1
block_size = 25
coef = [i/10.0 for i in range(10)]

''' 多组取平均 '''
group_num = 100
coef_num  = len(coef)
bmr = zeros((group_num,coef_num))
bgr = zeros((group_num,coef_num))

for i in range(group_num):
    for j in range(coef_num):
        print 'Running... Current group: ',i,j

        ''' 采样 '''
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time)

        ''' RSSI量化 '''
        bits_A,drop_list_A = quantize_ASBG_1bit(rssi_A,block_size,coef[j])
        bits_B,drop_list_B = quantize_ASBG_1bit(rssi_B,block_size,coef[j])
        bits_A = remain(bits_A,drop_list_A,drop_list_B)
        bits_B = remain(bits_B,drop_list_A,drop_list_B)

        ''' 评价性能 '''
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(coef,bmr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('BMR')
plt.title('BMR of different coef(bl=%d)'%(block_size))
plt.show()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('BGR')
plt.title('BGR of different coef(bl=%d)'%(block_size))
plt.ylim(0,1)
plt.show()

print 'Program Finished'
