# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:00:09 2016

@author: My402
"""

import numpy as np
import random
from numpy import dot,diag,zeros,repeat,shape
from numpy.random import randn
from numpy.fft import fft,ifft
from function import fftMatrix
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
    tau = random.sample(range(L),K)     # 取值范围[0,L-1]，不重复的P个随机整数
    tau.sort()
    tau[0] = 0                          # 规定第一个路径时延为0
    
    # 每条路径的增益呈复高斯分布
    ampli = randn(K) + 1j*randn(K)
    ampli = ampli/np.abs(ampli)

    h = zeros((L,1),dtype=np.complex)               # 信道的冲激响应是一个复数
    for i in range(K):
        h[tau[i]] = exp(-tau[i]/taumax)*ampli[i]    # 路径复增益的功率指数衰落
    return h
    
def awgn(X,SNR):
    SNR_log=10**(SNR/10.0)
    xpower=np.sum(X**2)/len(X)
    npower=xpower/SNR_log
    No=randn(len(X)) * np.sqrt(npower)
    Y = np.zeros(X.shape,X.dtype)
    for i in range(len(X)):
        Y[i]=X[i]+No[i]
    return Y
    
def transmission(x,L,K,N,M,Ncp,SNR):
    
    ''' 
    x: 发送端的发送信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    SNR: 信噪比
    '''
    
    ''' 时域的信道脉冲响应'''
    # 对于慢时变信道，在多个OFDM符号周期内，信道冲激响应保持不变
    h = channel(L,K)            # 1个符号周期内
    h = repeat(h,M,axis=1)      # 在M个符号周期内，h保持不变，因此将h做M次重复
     
    ''' 信道频率响应H '''
    W = fftMatrix((N+Ncp),L)    # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
    H = dot(W,h)                # 频率的冲激响应
    
    ''' 将时域的发送信号，变换到频域 '''
    x = x.reshape(-1,M)
    X = fft(x,axis=0)
    Y = zeros(shape(X),dtype=np.complex)
    
    ''' 时域上分别传输M个OFDM符号 '''
    for i in range(M):
        ''' 测量矩阵 '''
        # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
        X_diag = diag(X[:,i])
        
        ''' 理想信道传输 '''
        X_H = dot(X_diag,H[:,i])
        
        ''' 添加高斯白噪声，得接收信号向量Y '''
        Y[:,i]  = awgn(X_H,SNR)    # 加入复高斯白噪声,得到接收到的信号（频域表示）
        #No = Y-X_H                # Y = X*H + No
    
    ''' 将频域的接收信号，变换到时域 '''
    y = ifft(Y,axis=0)
    y = y.reshape(-1,1)
    
    return h,H,y