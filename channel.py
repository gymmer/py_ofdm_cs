# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:40:23 2016

@author: My402
"""

import numpy as np
from math import exp
from numpy.random import randn,randint

def channel(L,K):
    
    '''
    信道脉冲响应,得h
    输入参数：
        L: 信号长度
        K: 抽头数/稀疏度/多径数
    '''
    
    # 最大时延
    taumax = L                          # (1)
    
    # 随机产生各径延时,延时的位置是各径信号到达接收端的时刻。K径产生K个时延
    tau = randint(low=1,high=taumax,size=K)
    
    # 幅度
    ampli = randn(K) + 1j*randn(K)      #（2）

    h = np.zeros(L)+1j*0                # 信道的冲激响应是一个复数
    for i in range(K):
        h[tau[i]] = exp(-tau[i]/taumax)*ampli[i]   # 指数衰落
    return h

'''
 (1)对于数字信号传输多径时延的极限是一个数字信号周期，否则，波形展宽将会造成数字信号的码间干扰。
    http://baike.baidu.com/link?url=fA8NBlYhPzkZCT4bN57m2M0oqAWX4vtdlHFng8iOvok63X0eUrHN9j2N1XqHLbdUtxxhmVK8EBtji3eD0Y4TN_
 (2)关于为什么选用高斯分布（正态分布）的复数，请参考《A Novel Sparse Channel Estimation Method Based on Discriminant
    Analysis for OFDM System》II.A
'''