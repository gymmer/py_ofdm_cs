# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:05:04 2016

@author: My402
"""

from function import interpolation 
import numpy as np
import math
from numpy import mean,zeros,size,dot,diag,eye
from math import pi,e
from transmission import channel,awgn
from numpy.random import randn,seed
from function import fftMatrix
import random

seed(0)
def channel(L,K,N):
    
    '''
    信道脉冲响应,得h
    输入参数：
        L: 信号长度
        K: 抽头数/稀疏度/多径数
    '''
    
    # 最大时延
    tau_max = float(L)
    
    # 随机产生各径延时,延时的位置是各径信号到达接收端的时刻。K径产生K个时延
    tau = random.sample(range(L),K)     # 取值范围[0,L-1]，不重复的P个随机整数
    tau.sort()
    tau[0] = 0                          # 规定第一个路径时延为0
    
    # 最大多普勒单边频移
    doppler_max = N
    # 随机产生各径多普勒频移
    doppler = random.sample(range(-doppler_max/2,doppler_max/2),K)
    
    # 每条路径的增益呈复高斯分布
    ampli = randn(K) + 1j*randn(K)
    ampli = ampli/np.abs(ampli)

    h = zeros((N,L),dtype=np.complex)
    for n in range(N):
            h[n,:] = 
    #h = zeros(L,dtype=np.complex)                   # 信道的冲激响应是一个复数
    #for i in range(K):
    #    h[tau[i]] = exp(-tau[i]/taumax)*ampli[i]    # 路径复增益的功率指数衰落
    #return h