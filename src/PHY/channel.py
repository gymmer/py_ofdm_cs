# -*- coding: utf-8 -*-

import numpy as np
import random
from numpy import zeros,abs
from numpy.random import randn
from math import exp

def channel(L,K):
    
    '''
    信道脉冲响应,得h
    输入参数：
        L: 信号长度
        K: 抽头数/稀疏度/多径数
    '''
    
    # 最大时延
    taumax = float(L)
    
    # 随机产生各径延时,延时的位置是各径信号到达接收端的时刻。K径产生K个时延
    tau = random.sample(range(L),K)                 # 取值范围[0,L-1]，不重复的P个随机整数
    tau.sort()
    tau[0] = 0                                      # 规定第一个路径时延为0
    
    # 每条路径的增益呈复高斯分布
    ampli = randn(K) + 1j*randn(K)
    ampli = ampli/abs(ampli)

    h = zeros(L,dtype=np.complex)                   # 信道的冲激响应是一个复数
    for i in range(K):
        h[tau[i]] = exp(-tau[i]/taumax)*ampli[i]    # 路径复增益的功率指数衰落
    return h