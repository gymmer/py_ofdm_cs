# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,arange,savetxt,size

sys.path.append('../../src')
from util.metric import UST
from KG import sampling_RSSI,sampling_phase,quantize_phase,quantize_ASBG_1bit,remain,merge

os.system('cls')
plt.close('all')

''' 参数 '''
sampling_period = 1
sampling_time   = 20
mtype = ['RSSI', 'Phase', 'cross', 'and', 'or', 'xor', 'syn']

mtype_num = len(mtype)
ust = zeros(mtype_num)

''' 采样 ''' 
rssi_A, rssi_B, rssi_E  = sampling_RSSI( sampling_period,sampling_time)  
phase_A,phase_B,phase_E = sampling_phase(sampling_period,sampling_time)
    
''' RSSI量化 '''
bits_A_rssi,drop_list_A = quantize_ASBG_1bit(rssi_A)
bits_B_rssi,drop_list_B = quantize_ASBG_1bit(rssi_B)
bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)

''' Phase量化 '''
bits_A_phase = quantize_phase(phase_A)

''' 合并 '''
bits_A_cross = merge(bits_A_rssi,bits_A_phase,'cross')
bits_A_and   = merge(bits_A_rssi,bits_A_phase,'and')
bits_A_or    = merge(bits_A_rssi,bits_A_phase,'or')
bits_A_xor   = merge(bits_A_rssi,bits_A_phase,'xor')
bits_A_syn   = merge(bits_A_rssi,bits_A_phase,'syn')

''' 评价性能 '''
ust[0] = UST(bits_A_rssi)
ust[1] = UST(bits_A_phase)
ust[2] = UST(bits_A_cross)
ust[3] = UST(bits_A_and)
ust[4] = UST(bits_A_or)
ust[5] = UST(bits_A_xor)
ust[6] = UST(bits_A_syn)
    
''' 画图 '''
labels = ['RSSI Only', 'Phase Only', 'Cross', 'AND', 'OR', 'XOR', 'Syn']
plt.figure(figsize=(8,5))
for x,y in zip(arange(len(labels)),ust):
    plt.bar(x+1,ust[x],width=0.5,facecolor='lightgray',edgecolor='black')
    plt.text(x+1+0.25,y,'%s\n%.4f'%(labels[x],y),ha='center',va='bottom')
plt.xlim(0.5,8)
plt.ylim(0,1)
plt.xticks([])
plt.xlabel('Quantize Scheme')
plt.ylabel('P_value')
plt.title('Universal Statistical Test of different merge method')
plt.show()

''' 保存数据到文件，用于NIST测试 '''
os.chdir('../../dist')
savetxt( "bits_rssi_%d.txt"%size(bits_A_rssi), bits_A_rssi, fmt="%d")
savetxt("bits_phase_%d.txt"%size(bits_A_phase),bits_A_phase,fmt="%d")
savetxt("bits_cross_%d.txt"%size(bits_A_cross),bits_A_cross,fmt="%d")
savetxt(  "bits_and_%d.txt"%size(bits_A_and),  bits_A_and,  fmt="%d")
savetxt(   "bits_or_%d.txt"%size(bits_A_or),   bits_A_or,   fmt="%d")
savetxt(  "bits_xor_%d.txt"%size(bits_A_xor),  bits_A_xor,  fmt="%d")
savetxt(  "bits_syn_%d.txt"%size(bits_A_syn),  bits_A_syn,  fmt="%d")

print 'Program Finished'