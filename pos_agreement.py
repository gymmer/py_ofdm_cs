# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:20:11 2016

@author: My402
"""    
import numpy as np
from numpy import corrcoef,mod,array,floor,ceil,pi
from function import BMR
import RSSI
import Phase
from part_transmission import awgn
from from_to import from2seq_to10
from winnow import winnow
    
def get_pos_from_bits(bits,P,pos):
    pos_num = 0                             # 已生成的导频数。初始时未生成导频，为0
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
    pos = array([],dtype=np.int32)                      # 初始化导频图样pos为空
    pos = get_pos_from_bits(bits_rssi, P_rssi, pos)     # 从RSSI的密钥流产生导频，追加到pos中
    pos = get_pos_from_bits(bits_phase,P_phase,pos)     # 从Phase的密钥流产生导频，追加到pos中
    pos.sort()                                          # pos中包含有（P_rssi+P_phase）个不重复的导频
    return pos
    
def agreement(sampling_time,P,weight,iteration=3):
    
    # 根据权重，计算RSSI和Phase两种方式各自产生的导频
    P_rssi,P_phase = floor(weight*P), ceil((1-weight)*P)
    
    ''' 采样参数'''
    SNR = 30
    sampling_period_rssi  = 1
    sampling_period_phase = 10
    
    '''量化参数'''
    block_size = 200
    coef = 0.8
    qtype = 'gray'
    order = 2
    
    ''' winnow最大迭代次数'''
    #iteration = 3
    
    ''' RSSI 采样'''        
    rssi_A = RSSI.sampling(sampling_period_rssi,sampling_time,1)
    rssi_B = awgn(rssi_A,SNR)
    rssi_E = RSSI.sampling(sampling_period_rssi,sampling_time,3)  
    
    ''' Phase 采样'''    
    phase_A = Phase.sampling(sampling_period_phase,sampling_time)
    phase_B = mod(awgn(phase_A,SNR),2*pi)
    phase_E = Phase.sampling(sampling_period_phase,sampling_time)
    
    ''' RSSI量化'''
    bits_A_rssi,drop_listA = RSSI.quantization_thre(rssi_A,block_size,coef)
    bits_B_rssi,drop_listB = RSSI.quantization_thre(rssi_B,block_size,coef)
    bits_E_rssi,drop_listE = RSSI.quantization_thre(rssi_E,block_size,coef)
    bits_A_rssi = RSSI.remain(bits_A_rssi,drop_listA,drop_listB)
    bits_B_rssi = RSSI.remain(bits_B_rssi,drop_listA,drop_listB)
    bits_E_rssi = RSSI.remain(bits_E_rssi,array([]),drop_listE)
    
    ''' Phase量化'''
    bits_A_phase = Phase.quantization_even(phase_A,qtype,order)
    bits_B_phase = Phase.quantization_even(phase_B,qtype,order)
    bits_E_phase = Phase.quantization_even(phase_E,qtype,order)
    
    ''' winnow信息协调'''
    bits_A_rssi, bits_B_rssi  = winnow(bits_A_rssi, bits_B_rssi ,iteration)
    bits_A_phase,bits_B_phase = winnow(bits_A_phase,bits_B_phase,iteration)

    ''' 生成导频 '''
    posA = generate_pos(bits_A_rssi,bits_A_phase,P_rssi,P_phase)
    posB = generate_pos(bits_B_rssi,bits_B_phase,P_rssi,P_phase)
    posE = generate_pos(bits_E_rssi,bits_E_phase,P_rssi,P_phase)
    
    #print 'corrcoef of rssi  between AB and AE:',corrcoef(rssi_A, rssi_B, rowvar=0)[0,1],corrcoef(rssi_A, rssi_E, rowvar=0)[0,1]            
    #print 'corrcoef of phase between AB and AE:',corrcoef(phase_A,phase_B,rowvar=0)[0,1],corrcoef(phase_A,phase_E,rowvar=0)[0,1]   
    #print 'BMR of rssi and phase after winnow between AB:',BMR(bits_A_rssi,bits_B_rssi),BMR(bits_A_phase,bits_B_phase)
    
    return posA,posB,posE