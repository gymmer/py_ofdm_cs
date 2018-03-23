# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import dot,diag
from numpy.fft import fft,ifft
from default import *

sys.path.append('../')
from util.mathematics import fftMatrix
from util.function import awgn
from PHY import channel

def transmission(x,SNR,L=dL,K=dK,N=dN,Ncp=dNcp):
    ''' 
    x:   发送端的发送信号
    SNR: 信噪比
    L:   信道长度
    K:   稀疏度
    N:   子载波数
    Ncp: 循环前缀长度
    '''
    
    ''' 时域的信道脉冲响应'''
    h = channel(L,K)
    
    ''' 信道频率响应H '''
    W = fftMatrix(N,L)          # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
    H = dot(W,h)                # 频率的冲激响应
    H.shape = (N,1)
    
    ''' 不考虑循环前缀在信道中的传输 '''
    x = x[:,Ncp:]
    x = x.reshape(N)
    # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
    X = fft(x)
    
    ''' 测量矩阵 '''
    X = diag(X)
    
    ''' 理想信道传输 '''
    X_H = dot(X,H)
    
    ''' 添加高斯白噪声，得接收信号向量Y '''
    Y  = awgn(X_H,SNR)          # 加入复高斯白噪声,得到接收到的信号（频域表示）
    #No = Y-X_H                  # Y = X*H + No
    
    y = ifft(Y,axis=0)
    y = y.reshape(1,N)
    y = np.c_[y[:,-Ncp:],y]
    
    return h,H,y