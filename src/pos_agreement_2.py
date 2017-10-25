# -*- coding: utf-8 -*-
import numpy as np
from numpy import corrcoef,mod,array,floor,ceil,pi,size,zeros,mean
from function import BMR,how_many_equal
from security_sampling import sampling
from security_quantize import quantization_thre,quantization_even,remain
from security_winnow import winnow
from security_encode import encode
from security_merge import *

def agreement(P,mtype,iteration=2,corr_ab=0.9,corr_ae=0.4):
    '''
    P: 导频数
    mtype: 合并类型。RSSI/Phase/cross/and/or/xor
    iteration: winnow迭代次数
    corr_ab: Alice和Bob的信道测量值的相关系数
    corr_ae: Alice和Eve的信道测量值的相关系数
    '''
    
    ''' 采样参数 '''
    sampling_period_rssi  = 1
    sampling_period_phase = 10
    sampling_time = 4
    
    ''' 量化参数 '''
    block_size = 25
    coef = 0.8
    qtype = 'gray'
    order = 2
    
    ''' 采样 ''' 
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period_rssi,sampling_time,corr_ab,corr_ae)  
    phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period_phase,sampling_time,corr_ab,corr_ae),2*pi)
        
    ''' RSSI量化 '''
    bits_A_rssi,drop_listA = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_listB = quantization_thre(rssi_B,block_size,coef)
    bits_E_rssi,drop_listE = quantization_thre(rssi_E,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_listA,drop_listB)
    bits_B_rssi = remain(bits_B_rssi,drop_listA,drop_listB)
    bits_E_rssi = remain(bits_E_rssi,drop_listA,drop_listE)
    #print 'BMR of RSSI before winnow between AB',BMR(bits_A_rssi,bits_B_rssi)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
    bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
    bits_E_phase = quantization_even('Phase',phase_E,size(phase_E),qtype,order)
    #print 'BMR of phase before winnow between AB',BMR(bits_A_phase,bits_B_phase)
    
    ''' 合并 '''
    if mtype == 'RSSI':
        bits_A = bits_A_rssi
        bits_B = bits_B_rssi
        bits_E = bits_E_rssi
    elif mtype == 'Phase':
        bits_A = bits_A_phase
        bits_B = bits_B_phase
        bits_E = bits_E_phase
    else:
        if mtype == 'cross':
            merge_method = merge_cross
        elif mtype == 'and':
            merge_method = merge_and
        elif mtype == 'or':
            merge_method = merge_or
        elif mtype == 'xor':
            merge_method = merge_xor
        bits_A = merge_method(bits_A_rssi,bits_A_phase)
        bits_B = merge_method(bits_B_rssi,bits_B_phase)
        bits_E = merge_method(bits_E_rssi,bits_E_phase)
    #print 'BMR of merge before winnow between AB',BMR(bits_A,bits_B)
    
    ''' winnow信息协调 '''
    bits_A, bits_B = winnow(bits_A,bits_B,iteration)
    #print 'BMR of merge after winnow between AB',BMR(bits_A,bits_B)
    
    ''' 生成导频 '''
    pos_A = encode(bits_A,36)
    pos_B = encode(bits_B,36)
    pos_E = encode(bits_E,36)

    return pos_A,pos_B,pos_E

if __name__=='__main__':
    posA,posB,posE = agreement(36,'cross',1)
    print how_many_equal(posA,posB)
    print how_many_equal(posA,posE)