# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:20:11 2016

@author: My402
"""    
import numpy as np
from numpy import corrcoef,mod,array,floor,ceil,pi,size
from function import BMR,how_many_equal
from security_sampling import sampling
from security_quantize import quantization_thre,quantization_even,remain
from security_winnow import winnow
from from_to import from2seq_to10

def get_pos_from_bits(bits,P):
    pos_num = 0                             # 已生成的导频数。初始时未生成导频，为0
    pos = array([],dtype=np.int32)          # 初始化导频图样pos为空
    index = 0
    while(pos_num<P):                       # 循环停止的条件是，已经根据密钥流产生了足够数量的导频位置
        seed = bits[index*9:(index+1)*9]    # 如果N=512,则导频位置的取值范围[0,512]，需要对9位二进制转成十进制。
        index += 1
        new_pos = int(from2seq_to10(seed))  # 密钥流每读入9个比特，则计算一次新产生的导频位置
        if new_pos not in pos:              # 如果新增导频不在我的已有导频列表中，则加入这个导频
            pos = np.r_[pos,new_pos]        # 如果已有导频列表中已有该导频，则放弃。防止重复加入多个相同的同频位置
            pos_num += 1                    # 修改已产生的导频位置数
    return pos

def generate_pos(bits_rssi,bits_phase,P_rssi,P_phase):
    pos_phase = get_pos_from_bits(bits_phase,P_phase)   # 从Phase的密钥流产生导频
    pos_rssi = get_pos_from_bits(bits_rssi, P_rssi)     # 从RSSI的密钥流产生导频
    pos = np.r_[pos_phase,pos_rssi]
    pos.sort()                                          # pos中包含有（P_rssi+P_phase）个不重复的导频
    return pos
    
def agreement(P,weight,iteration=2,corr_ab=0.9,corr_ae=0.4):
    
    # 根据权重，计算RSSI和Phase两种方式各自产生的导频
    P_rssi,P_phase = floor(weight*P), ceil((1-weight)*P)
    
    ''' 采样参数 '''
    sampling_period_rssi  = 1
    sampling_period_phase = 10
    sampling_time = 3
    
    ''' 量化参数 '''
    block_size = 25
    coef = 0.8
    qtype = 'gray'
    order = 2
    
    ''' 采样 '''        
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period_rssi,sampling_time,corr_ab,corr_ae)  
    phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period_phase,sampling_time,corr_ab,corr_ae),2*pi)    
    #print 'corrcoef of rssi  between AB and AE:',corrcoef(rssi_A, rssi_B, rowvar=0)[0,1],corrcoef(rssi_A, rssi_E, rowvar=0)[0,1]            
    #print 'corrcoef of phase between AB and AE:',corrcoef(phase_A,phase_B,rowvar=0)[0,1],corrcoef(phase_A,phase_E,rowvar=0)[0,1]   
    
    ''' RSSI量化 '''
    bits_A_rssi,drop_listA = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_listB = quantization_thre(rssi_B,block_size,coef)
    bits_E_rssi,drop_listE = quantization_thre(rssi_E,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_listA,drop_listB)
    bits_B_rssi = remain(bits_B_rssi,drop_listA,drop_listB)
    #bits_E_rssi = remain(bits_E_rssi,array([]),drop_listE)
    bits_E_rssi = remain(bits_E_rssi,drop_listA,drop_listE)
    #print bits_A_rssi.shape,bits_B_rssi.shape,bits_E_rssi.shape
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    bits_E_phase = quantization_even('Phase',phase_E,size(phase_E),qtype,order)
    #print 'BMR of phase before winnow between AB and AE:',BMR(bits_A_phase,bits_B_phase),BMR(bits_A_phase,bits_E_phase)
    
    ''' winnow信息协调 '''
    bits_A_rssi, bits_B_rssi  = winnow(bits_A_rssi, bits_B_rssi ,iteration)
    bits_A_phase,bits_B_phase = winnow(bits_A_phase,bits_B_phase,iteration)

    ''' 生成导频 '''
    posA = generate_pos(bits_A_rssi,bits_A_phase,P_rssi,P_phase)
    posB = generate_pos(bits_B_rssi,bits_B_phase,P_rssi,P_phase)
    posE = generate_pos(bits_E_rssi,bits_E_phase,P_rssi,P_phase)    
    #print 'BMR of rssi and phase after winnow between AB:',BMR(bits_A_rssi,bits_B_rssi),BMR(bits_A_phase,bits_B_phase)
    
    return posA,posB,posE

if __name__=='__main__':
    posA,posB,posE = agreement(36,0.7)
    print how_many_equal(posA,posB)
    print how_many_equal(posA,posE)