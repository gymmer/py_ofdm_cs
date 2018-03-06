# -*- coding: utf-8 -*-

import sys
import os
import datetime
import matplotlib.pyplot as plt
from numpy import zeros,size,mod,pi

sys.path.append('../')
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')
    
''' 采样参数 '''
sampling_period = 1
sampling_time = range(1,30,1)

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 1
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

''' 多组取平均 '''
gro_num = 1
st_num = len(sampling_time)
mtype_num = len(mtype)
times = zeros((st_num,mtype_num))

for i in range(st_num):
    
    ''' 采样 '''
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time[i],0.9,0.4)
    phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time[i],0.9,0.4),2*pi)

    for j in range(mtype_num):
        
        print 'Running... Current group:',i,j
        begin = datetime.datetime.now()
        
        if mtype[j] == 'RSSI':
            ''' RSSI Only '''
            for k in range(gro_num):
                bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
                bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
                bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
                bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
            
        elif mtype[j] == 'Phase':
            for k in range(gro_num):
                ''' Phase Only '''
                bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
                bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
        
        else:
            for k in range(gro_num):
                ''' RSSI量化 '''
                bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
                bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
                bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
                bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
                
                ''' Phase量化 '''
                bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
                bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
                
                ''' 合并 '''
                bits_A = merge(bits_A_rssi,bits_A_phase,mtype[j])
                bits_B = merge(bits_B_rssi,bits_B_phase,mtype[j])
            
        end = datetime.datetime.now()
        # 转化成毫秒ms，并求每组样例的平均耗时。另Alice和Bob同时做量化，因此除2求每个人的耗时
        times[i,j] = (end-begin).total_seconds()*1000/gro_num/2

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