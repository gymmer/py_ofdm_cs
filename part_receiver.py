# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:06:33 2016

@author: My402
"""

import numpy as np
from numpy import dot,transpose,eye,size,zeros
from numpy.linalg import inv
from numpy.fft import fft
import matplotlib.pyplot as plt
from OMP import OMP
from function import fftMatrix,ifftMatrix,interpolation
import QAM16

def receiver(y,L,K,N,M,Ncp,pos,etype):

    '''
    y: 接收信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    pos: 导频图样
    etype: 'CS' 或 'LS'
    '''
    
    ''' 串并转换 '''
    y = y.reshape(-1,M)
    
    ''' 移除循环前缀'''
    y = y[Ncp:,:]
    
    ''' FFT '''
    Y = fft(y,axis=0)
    
    ''' 导频选择矩阵 '''
    P = size(pos)
    I = eye(N,N)            # NxN的单位矩阵
    S = I[pos,:]            # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
    ''' 提取导频 ''' 
    Yp = dot(S,Y)           # Px1的导频位置的接受信号向量
    #Xp = dot( dot(S,X), transpose(S) ) # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
    Xp = eye(P,P)
    W = fftMatrix(N,L)      # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基  
    Wp = dot(S,W)           # PxL的矩阵,从W中选取与导频位置对应的P行
    
    if etype=='CS':
        ''' CS信道估计'''
        # s   = Phi*Psi*x
        # Y   = X  * W *h + N
        #     = X  * H    + N
        # hat_H = omp(K,s,Phi,Psi)
        #   ==>   s   = Y
        #   ==>   Phi = X
        #   ==>   Psi = W
        
        # Xp*Wp作为密钥。若Xp是单位矩阵，则Xp*Wp=Wp，密钥取决于Wp。
        # 而Wp又是从W中选取的与导频位置对应的P行，所以密钥取决于导频位置pos
        re_h = zeros((L,M),dtype=np.complex) # OMP是时域估计算法，估计得到时域的h
        for i in range(M):                   # 第i个符号的CS重构的h。对于慢衰落信道，不同符号的重构h应该大致相同
            re_h[:,i] = OMP(K,Yp[:,i],Xp,Wp).reshape(L)
        re_H = dot(W,re_h)                   # 傅里叶变换，得到频域的H
    
    elif etype=='LS':       
        ''' LS信道估计 '''
        Hp_ls = dot(inv(Xp),Yp)              # LS、MMSE是频域估计算法，得到导频处的Hp
        
        re_H = zeros((N,M),dtype=np.complex) # 根据导频处Hp进行插值，恢复信道的H 
        for i in range(M):                   # 对第i个符号的Hp进行插值
            re_H[:,i] = interpolation(Hp_ls[:,i],pos,N)
        re_h = dot(ifftMatrix(L,N),re_H)     # 傅里叶逆变换，得到时域的h
    
    ''' 信道均衡 '''
    Y = Y/re_H
    
    ''' 并串转换 '''
    Y = Y.reshape(-1,1)
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(Y),np.imag(Y))
    plt.title('Constellation diagram of receiver')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 16-QAM解调 '''
    bits = QAM16.demod(Y)
    
    return re_h,re_H,bits