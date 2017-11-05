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
from security_encode import encode

def generate_pos(bits_rssi,bits_phase,P_rssi,P_phase):
    pos_phase = encode(bits_phase,P_phase)              # 从Phase的密钥流产生导频
    pos_rssi = encode(bits_rssi,P_rssi,pos_phase)       # 从RSSI的密钥流产生导频
    pos = np.r_[pos_phase,pos_rssi]
    pos.sort()                                          # pos中包含有（P_rssi+P_phase）个不重复的导频
    return pos
    
def agreement(P,weight,iteration=2,corr_ab=0.9,corr_ae=0.4):
    '''
    P: 导频数
    weight: 权重。RSSI权重weight，相位权重(1-weight)
    iteration: winnow迭代次数
    corr_ab: Alice和Bob的信道测量值的相关系数
    corr_ae: Alice和Eve的信道测量值的相关系数
    '''

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
    P_rssi,P_phase = floor(weight*P), ceil((1-weight)*P) # 根据权重，计算RSSI和Phase两种方式各自产生的导频
    posA = generate_pos(bits_A_rssi,bits_A_phase,P_rssi,P_phase)
    posB = generate_pos(bits_B_rssi,bits_B_phase,P_rssi,P_phase)
    posE = generate_pos(bits_E_rssi,bits_E_phase,P_rssi,P_phase)    
    #print 'BMR of rssi and phase after winnow between AB:',BMR(bits_A_rssi,bits_B_rssi),BMR(bits_A_phase,bits_B_phase)
    
    return posA,posB,posE

if __name__=='__main__':
    posA,posB,posE = agreement(36,0.7)
    print how_many_equal(posA,posB)
    print how_many_equal(posA,posE)