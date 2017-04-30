# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:00:09 2016

@author: My402
"""

import numpy as np
import random
from numpy import dot,diag,zeros,kron,eye
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

    h = zeros(L,dtype=np.complex)               # 信道的冲激响应是一个复数
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
    
def transmission(SEND,L,K,N,M,Ncp,Nt,Nr,SNR):
    
    ''' 
    SEND: 发送端的发送信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    Nt: 发送天线数
    Nr: 接收天线数
    SNR: 信噪比
    '''
    
    ''' 时域/频域的信道响应'''
    h = zeros((Nr,Nt,L),dtype=np.complex)
    H = zeros((Nr,Nt,N),dtype=np.complex)
    for r in range(Nr):
        for t in range(Nt):
            h[r,t,:] = channel(L,K)     # 第r个接收天线，与第t个发送天线的1个符号周期内的信道脉冲响应
            H[r,t,:] = dot(fftMatrix(N,L),h[r,t,:])     # 信道频率响应
     
    ''' 傅里叶正变换矩阵 '''
    W = fftMatrix((N+Ncp),L)            # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
    W_M = W                             # 对于慢时变信道，在M个符号周期内，H保持不变。相当于对W做M次重复
    for i in range(M-1):
        W_M = np.r_[W_M,W]    
    
    for t in range(Nt):
        
        ''' 第t个天线的发送数据 '''
        x = SEND[:,t]
        
        ''' 将时域的发送信号，变换到频域 '''
        X = fft(x)
        
        ''' 测量矩阵 '''
        # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
        X = diag(X)
        
        if t==0:
            X_wave = dot(X,W_M)
        else:
            X_wave = np.c_[X_wave,dot(X,W_M)]
    
    ''' X_wave与Nr*Nr单位矩阵的克罗内克积 '''    
    Kronecker = kron(eye(Nr,Nr),X_wave)
    
    ''' Nt*Nr*L的信道脉冲响应向量 '''
    for r in range(Nr):
        for t in range(Nt):
            h_rt = h[r,t,:].reshape(-1,1)   # 第r个接收天线，与第t个发送天线的1个符号周期内的信道脉冲响应
            if r==0 and t==0:
                h_vector = h_rt
            else:
                h_vector = np.r_[h_vector,h_rt]

    ''' 理想信道传输 '''
    Y = dot(Kronecker,h_vector)
    
    ''' AWGN '''
    Y = awgn(Y,SNR)    
    y = ifft(Y,axis=0)
    RECEIVE = y.reshape(-1,Nr)
    
    return h,H,RECEIVE