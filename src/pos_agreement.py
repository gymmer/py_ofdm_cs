# -*- coding: utf-8 -*-
import numpy as np
from numpy import corrcoef,mod,pi,size
from function import BMR,how_many_equal
from security_sampling import sampling
from security_quantize import quantization_thre,quantization_even,remain
from security_winnow import winnow
from security_encode import encode
from security_merge import merge

def agreement(P,mtype='cross',iteration=2,corr_ab=0.9,corr_ae=0.4):
    '''
    P: 导频数
    mtype: 合并类型。RSSI/Phase/cross/and/or/xor
    iteration: winnow迭代次数
    corr_ab: Alice和Bob的信道测量值的相关系数
    corr_ae: Alice和Eve的信道测量值的相关系数
    '''
    
    ''' 采样参数 '''
    sampling_period = 1
    sampling_time = 3
    
    ''' 量化参数 '''
    block_size = 25
    coef = 0.8
    qtype = 'gray'
    order = 1
    
    ''' 采样 ''' 
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,corr_ab,corr_ae)  
    phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,corr_ab,corr_ae),2*pi)
    #print 'corrcoef of rssi  between AB and AE:',corrcoef(rssi_A, rssi_B, rowvar=0)[0,1],corrcoef(rssi_A, rssi_E, rowvar=0)[0,1]
    #print 'corrcoef of phase between AB and AE:',corrcoef(phase_A,phase_B,rowvar=0)[0,1],corrcoef(phase_A,phase_E,rowvar=0)[0,1]
        
    ''' RSSI量化 '''
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_E_rssi,drop_list_E = quantization_thre(rssi_E,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
    bits_E_rssi = remain(bits_E_rssi,drop_list_A,drop_list_E)
    #print 'BMR of RSSI before winnow between AB',BMR(bits_A_rssi,bits_B_rssi)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    bits_E_phase = quantization_even('Phase',phase_E,size(phase_E),qtype,order)
    #print 'BMR of phase before winnow between AB',BMR(bits_A_phase,bits_B_phase)
    
    ''' 合并 '''
    bits_A = merge(bits_A_rssi,bits_A_phase,mtype)
    bits_B = merge(bits_B_rssi,bits_B_phase,mtype)
    bits_E = merge(bits_E_rssi,bits_E_phase,mtype)
    #print 'BMR of merge before winnow between AB',BMR(bits_A,bits_B)
    
    ''' winnow信息协调 '''
    bits_A, bits_B = winnow(bits_A,bits_B,iteration)
    #print 'BMR of merge after winnow between AB',BMR(bits_A,bits_B)
    
    ''' 生成导频 '''
    pos_A = encode(bits_A,P)
    pos_B = encode(bits_B,P)
    pos_E = encode(bits_E,P)

    return pos_A,pos_B,pos_E

if __name__=='__main__':
    posA,posB,posE = agreement(36,'cross',1)
    print how_many_equal(posA,posB)
    print how_many_equal(posA,posE)