# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

import numpy as np
from numpy.random import randn
from RSSI import sampling,quantization,hash_tiger
from RC4 import RC4

def sender (N,P,ptype):
    
    ''' 发送端序列的频谱Xn '''
    Xn = randn(N)           # 均值为0，方差为1的正态分布
    
    ''' 导频位置 '''    
    if ptype == 'random':       # 随机，根据RSSI生成导频位置
        RSSI = sampling(1,1,1)
        bit = quantization(RSSI,2,1)
        key = hash_tiger(bit)
        pos = RC4(key,P)
    elif ptype == 'even':       # 均匀
        pos = np.arange(P)*5    # 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个
 
    ''' 插入导频,导频位置设为1 '''
    Xn[pos] = 1
    
    return Xn,pos