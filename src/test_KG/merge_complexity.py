# -*- coding: utf-8 -*-

import sys
import os
import datetime
import matplotlib.pyplot as plt
from numpy import zeros

sys.path.append('../')
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')
    
''' 参数 '''
sampling_period = 1
sampling_time   = range(1,30,1)
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

''' 多组取平均 '''
group_num = 1
stime_num = len(sampling_time)
mtype_num = len(mtype)
times     = zeros((stime_num,mtype_num))

for i in range(stime_num):
    
    ''' 采样 '''
    rssi_A, rssi_B, rssi_E  = sampling('RSSI', sampling_period,sampling_time)  
    phase_A,phase_B,phase_E = sampling('Phase',sampling_period,sampling_time)

    for j in range(mtype_num):
        
        print 'Running... Current group:',i,j
        begin = datetime.datetime.now()
        
        if mtype[j] == 'RSSI':
            for k in range(group_num):
                ''' RSSI Only '''
                bits_A_rssi,drop_list_A = quantization_thre(rssi_A)
                bits_B_rssi,drop_list_B = quantization_thre(rssi_B)
                bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
                bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
            
        elif mtype[j] == 'Phase':
            for k in range(group_num):
                ''' Phase Only '''
                bits_A_phase = quantization_even(phase_A)
                bits_B_phase = quantization_even(phase_B)
        
        else:
            for k in range(group_num):
                ''' RSSI量化 '''
                bits_A_rssi,drop_list_A = quantization_thre(rssi_A)
                bits_B_rssi,drop_list_B = quantization_thre(rssi_B)
                bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
                bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
                
                ''' Phase量化 '''
                bits_A_phase = quantization_even(phase_A)
                bits_B_phase = quantization_even(phase_B)
                
                ''' 合并 '''
                bits_A = merge(bits_A_rssi,bits_A_phase,mtype[j])
                bits_B = merge(bits_B_rssi,bits_B_phase,mtype[j])
            
        end = datetime.datetime.now()
        # 转化成毫秒ms，并求每组样例的平均耗时。另Alice和Bob同时做量化，因此除2求每个人的耗时
        times[i,j] = (end-begin).total_seconds()*1000/group_num/2

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(sampling_time,times[:,0],'ko-', label='RSSI Only')
plt.plot(sampling_time,times[:,1],'k^:', label='Phase Only')
plt.plot(sampling_time,times[:,2],'ks--',label='Cross')
plt.xlabel('Sampling Time(s)')
plt.ylabel('Time(ms)')
plt.title('Time of different sampling time')
plt.legend()
plt.show()

print 'Program Finished'