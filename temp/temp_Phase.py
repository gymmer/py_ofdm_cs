# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import size,array,pi,zeros,corrcoef
from Phase_quantization_nbit import *
from part_transmission import awgn

def sampling(sampling_period,sampling_time,corr):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个Phase样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    corr:            在给定相关系数corr时，得到与Phase_A满足corr的Phase_B(或Phase_E)    
    '''
    corr_SNR_dict={
    0.1:10, 0.2:16, 0.3:20, 0.4:23, 0.5:25,
    0.6:27, 0.7:30, 0.8:32, 0.9:36, 1.0:1000
    }
    
    sampling_num = sampling_time*1000/sampling_period
    Phase = 2*pi*np.random.random(sampling_num)     # [0,2pi)之间均匀分布
    SNR = corr_SNR_dict[corr]
    Phase = awgn(array(Phase),SNR)    
    return Phase

def draw_SNR_corr(sampling_period=10,sampling_time=2):
    
    SNR = range(-30,31,1)
    SNR_num = len(SNR)
    group = 100
    corr = zeros((group,SNR_num))
    Phase_A = sampling(sampling_period,sampling_time,1.0)
    
    for i in range(group):
        print 'running...',i
        for j in range(SNR_num):
            Phase_B = awgn(Phase_A,SNR[j])
            corr[i,j] = corrcoef(Phase_A,Phase_B,rowvar=0)[0,1]
    corr = mean(corr,0)
    
    plt.figure(figsize=(8,5))
    plt.plot(SNR,corr,'bo-')
    plt.xlabel('SNR')
    plt.ylabel('Corrcoef')
    plt.title('Corrcoef in different SNR')
    
def quantization_even(Phase,qtype,order):
    '''
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
        
    # 由于相位是均匀分布的，即使分成多个block，每个block中均匀量化的minimun=0,interval=2pi/(2^N)
    # 即不同block的minumum和interval均相同，划分多个block、在每个block中动态调整minimum和interval是没有意义的。
    # 由于分block与不分block的结果相同，所以，对相位进行量化时，不必分成block
    # 在进行分析时，不必考察block_size，只需关注量化阶数order
    bit_stream = array([],dtype=np.int32)        
    for i in range(size(Phase)):
        bit = quantize(Phase[i])
        bit_stream = np.r_[bit_stream,bit]           
            
    return bit_stream