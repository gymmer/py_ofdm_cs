# -*- coding: utf-8 -*-

import numpy as np
from numpy import size,array,mean,std,append,pi
from quantization_nbit import *
    
def remain(bits,drop_list_A,drop_list_B):
    drop_list_both = append(drop_list_A,drop_list_B)
    bits_remain = array([],dtype=bits.dtype)
    for i in range(size(bits)):
        if i not in drop_list_both:
            bits_remain = np.r_[bits_remain,bits[i]]
    return bits_remain
  
def quantization_even(stype,samples,block_size,qtype,order):
    '''
    均匀量化
    stype:
        RSSI: 对RSSI做均匀量化
        Phase: 对相位做均匀量化
    samples: 采样点
    block_size: 将samples划分成长为block_size的多个block
    qtype:
        gray: 均匀量化、格雷编码
        natural: 均匀量化、自然编码
    order: 量化阶数，order=1，2，3，4
        若order=1，则格雷编码与自然编码等价
    返回值: bit_stream，量化后的比特流
    '''
    
    # 由于相位是均匀分布的，即使分成多个block，每个block中均匀量化的minimun=0,interval=2pi/(2^N)
    # 即不同block的minumum和interval均相同，划分多个block、在每个block中动态调整minimum和interval是没有意义的。
    # 由于分block与不分block的结果相同，所以，对相位进行量化时，不必分成block
    # 在进行分析时，不必考察block_size，令block_size=size(samples).只需关注量化阶数order
    
    if qtype=='natural':
        if order==4:
            quantize = naturalCode_4bit
        elif order==3:
            quantize = naturalCode_3bit
        elif order==2:
            quantize = naturalCode_2bit
        elif order==1:
            quantize = Code_1bit                
    elif qtype=='gray':
        if order==4:
            quantize = grayCode_4bit
        elif order==3:
            quantize = grayCode_3bit
        elif order==2:
            quantize = grayCode_2bit
        elif order==1:
            quantize = Code_1bit

    block_num  = size(samples)/block_size
    bit_stream = array([],dtype=np.int32)
    
    for i in range(block_num):
        samples_bl  = samples[i*block_size:(i+1)*block_size]        # 每个block中的样本
        if stype=='RSSI':
            minimum,maxmum = min(samples_bl),max(samples_bl)        # 每个block中的最值
        elif stype=='Phase':
            minimum,maxmum = 0,2*pi
        interval = (maxmum-minimum)/(2.0**order)   # 每个block的量化间隔
        
        for j in range(block_size):
            bit = quantize(minimum,interval,samples_bl[j])
            bit_stream = np.r_[bit_stream,bit]

    return bit_stream

def quantization_thre(samples,block_size,coef):
    '''
    阈值量化
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