# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

import numpy as np
from numpy.random import randn
from RSSI import sampling,quantization_lossy
from A51 import A51

def sender (N,P,ptype,seed):
    
    ''' 发送端序列的频谱Xn '''
    Xn = randn(N)           # 均值为0，方差为1的正态分布
    
    ''' 导频位置 '''    
    if ptype == 'random':       # 随机，根据RSSI生成导频位置
        RSSI = sampling(200,seed,3,-63,-53)
        bit = quantization_lossy(RSSI)
        pos = A51(N,P,bit)
    elif ptype == 'even':       # 均匀
        pos = np.arange(P)*5    # 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个
 
    ''' 插入导频,导频位置设为1 '''
    Xn[pos] = 1
    
    return Xn,pos