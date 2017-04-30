# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import size,array
from Phase_quantization_nbit import *
  
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