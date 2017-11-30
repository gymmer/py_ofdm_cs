# -*- coding: utf-8 -*-

import sys
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from numpy import size,arange,mod,pi

sys.path.append('../')
from KG import sampling,quantization_even,quantization_thre,remain,merge

os.system('cls')
plt.close('all')

''' 采样参数 '''
sampling_period  = 1
sampling_time = 3

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 1
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or']

''' 多组取平均 '''
gro_num = 100
mtype_num = len(mtype)
times = []

''' 采样 ''' 
rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)  
phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.9,0.4),2*pi)
    
''' RSSI Only '''
begin = datetime.datetime.now()
for i in range(gro_num):
    print 'Running... Current group: RSSI Only, ',i
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
end = datetime.datetime.now()
times.append(end-begin)

''' Phase Only '''
begin = datetime.datetime.now()
for i in range(gro_num):
    print 'Running... Current group: Phase Only, ',i
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
end = datetime.datetime.now()
times.append(end-begin)

''' cross '''
begin = datetime.datetime.now()
for i in range(gro_num):
    print 'Running... Current group: cross, ',i
    
    ''' RSSI量化 '''
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    
    ''' 合并 '''
    bits_A = merge(bits_A_rssi,bits_A_phase,'cross')
    bits_B = merge(bits_B_rssi,bits_B_phase,'cross')
end = datetime.datetime.now()
times.append(end-begin)

''' and '''
begin = datetime.datetime.now()
for i in range(gro_num):
    print 'Running... Current group: and, ',i
    
    ''' RSSI量化 '''
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    
    ''' 合并 '''
    bits_A = merge(bits_A_rssi,bits_A_phase,'and')
    bits_B = merge(bits_B_rssi,bits_B_phase,'and')
end = datetime.datetime.now()
times.append(end-begin)

''' or '''
begin = datetime.datetime.now()
for i in range(gro_num):
    print 'Running... Current group: or, ',i
    
    ''' RSSI量化 '''
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    
    ''' 合并 '''
    bits_A = merge(bits_A_rssi,bits_A_phase,'or')
    bits_B = merge(bits_B_rssi,bits_B_phase,'or')
end = datetime.datetime.now()
times.append(end-begin)

# 转化成毫秒ms，并求每组样例的平均耗时。另Alice和Bob同时做量化，因此除2求每个人的耗时
for i in range(mtype_num):
    times[i] = times[i].total_seconds()*1000/gro_num/2

''' 画图 '''
plt.figure(figsize=(8,5))
color = ['r','g','b','c','y']
for x,y in zip(arange(mtype_num),times):
    plt.bar(x+1,times[x],width=0.5,facecolor=color[x],edgecolor='white',label='%s'%(mtype[x]))
    plt.text(x+1+0.25,y,'%d'%y,ha='center',va='bottom')
plt.xlim(0.5,7.5)
plt.ylim(0,230)
plt.xticks([])
plt.xlabel('Merge method')
plt.ylabel('Time(ms)')
plt.title('Time of different merge method')
plt.legend()
plt.show()

print 'Program Finished'