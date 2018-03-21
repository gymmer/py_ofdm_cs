# -*- coding: utf-8 -*-

import sys

sys.path.append('../')
from util.function import how_many_equal
from sampling import sampling
from quantize import quantization_thre,quantization_even,remain
from merge import merge
from reconciliation import reconciliation
from encode import encode

def agreement(P,config={}):
    '''
    P: 导频数
    config: 密钥生成配置项，包括：
        sampling_period：采样周期
        sampling_time：采样时间
        corr_ab: Alice和Bob的信道测量值的相关系数
        corr_ae: Alice和Eve的信道测量值的相关系数
        block_size：双阈值量化的子块采样点数
        coef: 双阈值量化的量化系数
        qtype: 均匀量化的编码方式。gray/natural
        order: 均匀量化的量化阶数
        mtype: 合并类型。RSSI/Phase/cross/and/or/xor
        rtype: 信息协调方式。cascade/winnow
        iteration: 信息协调迭代次数
    '''
    
    ''' 采样参数 '''
    sampling_period = config.get('sampling_period', 1)
    sampling_time   = config.get('sampling_time', 3)
    corr_ab = config.get('corr_ab', 0.9)
    corr_ae = config.get('corr_ae', 0.4)
    
    ''' 量化参数 '''
    block_size = config.get('block_size', 25)
    coef  = config.get('coef', 0.8)
    qtype = config.get('qtype', 'gray')
    order = config.get('order', 1)
    mtype = config.get('mtype', 'cross')
    
    ''' 信息协调参数 '''
    rtype = config.get('rtype', 'winnow')
    iteration = config.get('iteration', 2)

    ''' 采样 ''' 
    rssi_A, rssi_B, rssi_E  = sampling('RSSI', sampling_period,sampling_time,corr_ab,corr_ae)  
    phase_A,phase_B,phase_E = sampling('Phase',sampling_period,sampling_time,corr_ab,corr_ae)

    ''' RSSI量化 '''
    bits_A_rssi,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_E_rssi,drop_list_E = quantization_thre(rssi_E,block_size,coef)
    bits_A_rssi = remain(bits_A_rssi,drop_list_A,drop_list_B)
    bits_B_rssi = remain(bits_B_rssi,drop_list_A,drop_list_B)
    bits_E_rssi = remain(bits_E_rssi,drop_list_A,drop_list_E)
    
    ''' Phase量化 '''
    bits_A_phase = quantization_even(phase_A,qtype,order)
    bits_B_phase = quantization_even(phase_B,qtype,order)
    bits_E_phase = quantization_even(phase_E,qtype,order)
    
    ''' 合并 '''
    bits_A = merge(bits_A_rssi,bits_A_phase,mtype)
    bits_B = merge(bits_B_rssi,bits_B_phase,mtype)
    bits_E = merge(bits_E_rssi,bits_E_phase,mtype)
    
    ''' 信息协调 '''
    bits_A,bits_B = reconciliation(bits_A,bits_B,rtype,iteration)
    
    ''' 生成导频 '''
    pos_A = encode(bits_A,P)
    pos_B = encode(bits_B,P)
    pos_E = encode(bits_E,P)

    return pos_A,pos_B,pos_E

if __name__=='__main__':
    posA,posB,posE = agreement(36)
    print how_many_equal(posA,posB)
    print how_many_equal(posA,posE)