# -*- coding: utf-8 -*-

import numpy as np
from math import floor
from numpy import size,array,mean,std,append,pi
from quantize_array import *

def quantize_even(samples,minimum,maxmum,qtype,order):
    ''' 均匀量化 '''
    bit_stream = array([],dtype=np.int32)
    interval = (maxmum-minimum)/(2.0**order)                 # 量化间隔
    code_array = eval('%s_%dbit_array'%(qtype,order))        # 编码矩阵
    
    for i in range(size(samples)):
        index = int(floor((samples[i]-minimum)/interval))    # 落在第index个区间
        bit = code_array[index]                              # 该区间的编码
        bit_stream = np.r_[bit_stream,bit]

    return bit_stream

def quantize_phase(samples,qtype='gray',order=1):
    '''
    相位量化
    samples: 采样点
    qtype: 编码方式。gray: 格雷编码。natural:自然编码。
    order: 量化阶数。若order=1，则格雷编码与自然编码等价
    返回值: 量化后的比特流
    '''
    
    minimum,maxmum = 0,2*pi
    return quantize_even(samples,minimum,maxmum,qtype,order)

def quantize_ASBG_nbit(samples,qtype='gray',order=2):
    '''
    多比特ASBG量化
    samples: 采样点
    qtype: 编码方式。gray: 格雷编码。natural:自然编码。
    order: 量化阶数。若order=1，则格雷编码与自然编码等价
    返回值: 量化后的比特流
    '''
    
    minimum,maxmum = min(samples),max(samples)+1        # 最大与最小值
    return quantize_even(samples,minimum,maxmum,qtype,order)
    
def quantize_ASBG_1bit(samples,block_size=25,coef=0.8):
    '''
    1比特ASBG
    samples: 采样点
    block_size: 将RSSI划分成长为block_size的多个block
    coef:量化系数，上阈值=均值+系数x标准差，下阈值=均值-系数x标准差
        阈值量化时，若para=0，则双阈值等价为单阈值，阈值=均值
    返回值: bit_stream，量化后的比特流
    '''
    # They drop RSS esimates that lie between two thresholds and maintain
    # a list of indices to track the RSS estimates that are dropped.
    # They exchange their list of dropped RSS estimates and 
    # only keep th ones that they both decide not to drop.
    block_num  = size(samples)/block_size
    bit_stream = array([],dtype=np.int32)
    drop_list  = array([],dtype=np.int32)
    
    for i in range(block_num):
        samples_bl = samples[i*block_size:(i+1)*block_size]       # 每个block中RSSI的样本
        mean_val   = mean(samples_bl)                             # 均值
        std_val    = std(samples_bl)                              # 标准差
        upper      = mean_val+coef*std_val                        # 上阈值
        lower      = mean_val-coef*std_val                        # 下阈值
        
        for j in range(block_size):
            if samples_bl[j] >= upper:
                bit_stream = np.r_[bit_stream,1]
            elif samples_bl[j] <= lower:
                bit_stream = np.r_[bit_stream,0]
            else:
                bit_stream = np.r_[bit_stream,-100]               # 用来临时填充
                drop_list = np.r_[drop_list,i*block_size+j]
      
    return bit_stream,drop_list

def remain(bits,drop_list_A,drop_list_B):
    drop_list_both = append(drop_list_A,drop_list_B)
    bits_remain = array([],dtype=bits.dtype)
    for i in range(size(bits)):
        if i not in drop_list_both:
            bits_remain = np.r_[bits_remain,bits[i]]
    return bits_remain