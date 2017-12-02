# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import dot,diag,zeros,kron,eye
from numpy.fft import fft,ifft

sys.path.append('../')
from util.mathematics import fftMatrix
from util.function import awgn
from PHY import channel

def transmission(x,L,K,N,M,Ncp,Nt,Nr,SNR):
    
    ''' 
    x: 发送端的发送信号
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
            h[r,t,:] = channel(L,K)         # 第r个接收天线，与第t个发送天线的1个符号周期内的信道脉冲响应
            H[r,t,:] = dot(fftMatrix(N,L),h[r,t,:])     # 信道频率响应
     
    ''' 傅里叶正变换矩阵 '''
    W = fftMatrix((N+Ncp),L)                # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
    W_M = W                                 # 对于慢时变信道，在M个符号周期内，H保持不变。相当于对W做M次重复
    for i in range(M-1):
        W_M = np.r_[W_M,W]    
    
    for t in range(Nt):
        
        ''' 第t个天线的发送数据 '''
        x_t = x[:,t]
        
        ''' 将时域的发送信号，变换到频域 '''
        X_t = fft(x_t)
        
        ''' 测量矩阵 '''
        X_t = diag(X_t)                     # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
        
        if t==0:
            X_wave = dot(X_t,W_M)
        else:
            X_wave = np.c_[X_wave,dot(X_t,W_M)]
    
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

    y = Y.reshape(-1,Nr)
    y = ifft(y,axis=0)

    return h,H,y