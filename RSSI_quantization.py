# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import size,array,mean,std,append
from RSSI_quantization_nbit import *

def remain(bits,drop_list_A,drop_list_B):
    drop_list_both = append(drop_list_A,drop_list_B)
    bits_remain = array([],dtype=bits.dtype)
    for i in range(size(bits)):
        if i not in drop_list_both:
            bits_remain = np.r_[bits_remain,bits[i]]
    return bits_remain
  
def quantization_even(RSSI,block_size,qtype,order):
    '''
    block_size : 将RSSI划分成长为block_size的多个block
    qtype:
        gray:均匀量化、格雷编码
        natural：均匀量化、自然编码
    order:量化阶数，order=1，2，3，4
        若order=1，则格雷编码与自然编码等价
    返回值：bit_stream，量化后的比特流
    '''
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
            
    block_num  = size(RSSI)/block_size
    bit_stream = array([],dtype=np.int32)
    
    for i in range(block_num):
        RSSI_bl  = RSSI[i*block_size:(i+1)*block_size]          # 每个block中RSSI的样本
        minimum  = min(RSSI_bl)                                 # 每个block中的最小值
        interval = (max(RSSI_bl)-min(RSSI_bl))/(2.0**order)     # 每个block的量化间隔
        
        for j in range(block_size):
            bit = quantize(minimum,interval,RSSI_bl[j])
            bit_stream = np.r_[bit_stream,bit]
            
    return bit_stream

def quantization_thre(RSSI,block_size,coef):
    '''
    block_size : 将RSSI划分成长为block_size的多个block
    coef:量化系数，上阈值=均值+系数x标准差，下阈值=均值-系数x标准差
        阈值量化时，若para=0，则双阈值等价为单阈值，阈值=均值
    返回值：bit_stream，量化后的比特流
    '''
    # They drop RSS esimates that lie between two thresholds and maintain
    # a list of indices to track the RSS estimates that are dropped.
    # They exchange their list of dropped RSS estimates and 
    # only keep th ones that they both decide not to drop.     
    block_num  = size(RSSI)/block_size
    bit_stream = array([],dtype=np.int32)
    drop_list  = array([],dtype=np.int32)
    
    for i in range(block_num):
        RSSI_bl = RSSI[i*block_size:(i+1)*block_size]   # 每个block中RSSI的样本
        upper = mean(RSSI_bl)+coef*std(RSSI_bl)            # 上阈值
        lower = mean(RSSI_bl)-coef*std(RSSI_bl)            # 下阈值
        
        for j in range(block_size):
            if RSSI_bl[j] >= upper:
                bit_stream = np.r_[bit_stream,1]
            elif RSSI_bl[j] <= lower:
                bit_stream = np.r_[bit_stream,0]
            else:
                bit_stream = np.r_[bit_stream,-100]       # 用来临时填充
                drop_list = np.r_[drop_list,i*block_size+j]
      
    return bit_stream,drop_list