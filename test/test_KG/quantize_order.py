# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.metric import BMR,BGR
from KG import sampling_phase,quantize_phase

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 1
order = [1,2,3,4,5]
qtype = ['natural','gray']

''' 多组取平均 '''
group_num = 100
order_num = len(order)
qtype_num = len(qtype)
bmr = zeros((group_num,order_num,qtype_num))
bgr = zeros((group_num,order_num,qtype_num))

for i in range(group_num):
    for j in range(order_num):
        for k in range(qtype_num):
            print 'Running... Current group: ',i,j,k
        	
            ''' 采样 '''
            phase_A,phase_B,phase_E = sampling_phase(sampling_period,sampling_time)

            ''' Phase量化 '''
            bits_A = quantize_phase(phase_A,qtype[k],order[j])
            bits_B = quantize_phase(phase_B,qtype[k],order[j])    
            
            ''' 评价性能 '''
            bmr[i,j,k] = BMR(bits_A,bits_B)
            bgr[i,j,k] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(order,bmr[:,0],'ko-',label=qtype[0])
plt.plot(order,bmr[:,1],'k^:',label=qtype[1])
plt.ylim(0,0.2)
plt.xlabel('Quantize Order')
plt.ylabel('BMR')
plt.title('BMR of different order')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(order,bgr[:,0],'ko-',label=qtype[0])
plt.plot(order,bgr[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BGR')
plt.title('BGR of different order')
plt.legend()
plt.show()

print 'Program Finished'
