# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:04:31 2016

@author: My402
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from numpy import size,dot,mean,diag,zeros,transpose,var,conjugate
from numpy.random import randn
from omp import omp
from math import pi,e
from LS_MSE_calc import LS_MSE_calc
from MMSE_MSE_calc import MMSE_MSE_calc
        
def awgn(X,snr):
    snr_log=10**(snr/10.0)
    xpower=np.sum(X**2)/len(X)
    npower=xpower/snr_log
    noise=randn(len(X)) * np.sqrt(npower)
    Y = np.zeros(X.shape,X.dtype)
    for i in range(len(X)):
        Y[i]=X[i]+noise[i]
    return Y

def fftMatrix(N,L):
    W = np.zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            W[n,l] = e**(-1j*2*pi*n*l/N)
    W = 1/math.sqrt(N)*W
    return W
    
def ifftMatrix(N,L):
    w = np.zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            w[n,l] = e**(1j*2*pi*n*l/L)
    w = 1/math.sqrt(L)*w
    return w
    
def MSE_com(K,h,SNR,N):
    '''
    LS/MMSE/CS信道估计，得MSE
    输入参数
        K:  稀疏度
        h:  信道脉冲响应
        SNR: AWGN信道信噪比
        N:  训练序列长度/载波数
        基本公式：Y = X*H + No = X*W*h + No
    '''
    L,SNR_num,group_num = size(h),size(SNR),20

    ''' 信道频率响应H '''
    W = fftMatrix(N,L)      # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
    H = dot(W,h)            # 频率的冲激响应
    H.shape = (N,1)
          
    ''' 发送端序列的频谱Xn '''
    Xn = randn(N)           # 均值为0，方差为1的正态分布
        
    ''' 测量矩阵,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵 '''
    X = diag(Xn)
    
    ''' 求h的自协方差矩阵-Rhh  '''
    gg = diag(h)
    
    gg_myu = np.sum(gg,0)/L  
    gg_myu.shape = (L,1)
    gg_myu_t = conjugate(transpose(gg_myu))
    
    gg_myu_expend = gg_myu_t   # gg_myu是一个1xL行向量，gg_myu_expend是一个LxL矩阵，其每一行都是gg_myu
    for i in range(L-1):
        gg_myu_expend = np.r_[gg_myu_expend,gg_myu_t]
        
    gg_mid   = gg-gg_myu_expend
    gg_mid_t = conjugate(transpose(gg_mid))
    
    sum_gg_mid = np.sum(gg_mid,0);
    sum_gg_mid.shape = (1,L)
    sum_gg_mid_t = conjugate(transpose(sum_gg_mid))
    
    Rgg = (dot(gg_mid_t,gg_mid) - dot(sum_gg_mid_t,sum_gg_mid)/L) / (L-1)
    
    ''' 信道估计 '''
    cs_mse   = zeros((group_num,SNR_num))
    ls_mse   = zeros((group_num,SNR_num))
    mmse_mse = zeros((group_num,SNR_num))
    
    for i in range(group_num):          # 多组实验取平均
        for j in range(SNR_num):        # 比较不同的信噪比
        
            ''' 添加高斯白噪声，得接收信号向量Y '''
            X_H = dot(X,H);             # 理想信道传输,X_H = X*H
            Y = awgn(X_H,SNR[j])        # 高斯白噪声
            No = Y-X_H                  # Y = X*H + No
            var_No = var(No);
            
            ''' CS信道估计H，得MSE'''
            # s   = Phi*Psi*x
            # Y   = X  * W *h + N
            #     = X  * H    + N
            # hat_H = omp(K,s,Phi,Psi)
            #   ==>   s   = Y;  
            #   ==>   Phi = X;
            #   ==>   Psi = W; 
                       
            re_H = omp(K,Y,X,W)
            diff_value = np.abs(re_H-H)           
            re_error = mean((diff_value/np.abs(H))**2)
            cs_mse[i,j] = re_error
            
            ''' LS信道估计 '''
            ls_mse[i,j] = LS_MSE_calc(X,H,Y,N)
            
            ''' MMSE信道估计 '''
            mmse_mse[i,j] = MMSE_MSE_calc(X,H,Y,Rgg,var_No,N,L)
    
    cs_mse_ave   = mean(cs_mse,0)
    ls_mse_ave   = mean(ls_mse,0)
    mmse_mse_ave = mean(mmse_mse,0)
        
    ''' 画图 '''
    if N==128:
        ''' 假设非法用户用另一个测量矩阵X进行解码 '''
        X_invalid = diag(randn(N))
        re_H_invalid = omp(K,Y,X_invalid,W)
        re_h = dot(ifftMatrix(L,N),re_H)
        re_h_invalid = dot(ifftMatrix(L,N),re_H_invalid)
    
        ''' 信道冲激响应 '''
        plt.figure(figsize=(10,9))
        plt.subplot(311)
        plt.stem(np.abs(h),'b')
        plt.title('Wireless Sparse Mutipath Channel in T Doamin(h)')
        plt.ylabel('Channel Impulse Response-CIR')
        plt.show()

        plt.subplot(312)
        plt.stem(np.abs(re_h),'g')
        plt.title('Reconstruct h after CS/OMP')
        plt.show()
        
        plt.subplot(313)
        plt.stem(np.abs(re_h_invalid),'r')
        plt.title('Reconstruct h of Invalid User')
        plt.xlabel('Sampling Point(Time Delay)')
        plt.show()
        
        ''' 信道频率响应 '''
        plt.figure(figsize=(10,9))
        plt.subplot(311)
        plt.plot(np.abs(H),'bo-')
        plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
        plt.ylabel('Channel Frequency Response')
        plt.show()
        
        plt.subplot(312)
        plt.plot(np.abs(re_H),'go-')        
        plt.title('Reconstruct H after CS/OMP')
        plt.show()
           
        plt.subplot(313)
        plt.plot(np.abs(re_H_invalid),'ro-')
        plt.title('Reconstruct H of Invalid User')
        plt.xlabel('Subcarrier Index')
        plt.show()
        
        ''' 发送、接收序列 '''
        plt.figure(figsize=(10,9))
        plt.subplot(221)
        plt.plot(np.abs(Xn),'bo-')
        plt.title('X')
        plt.ylabel('Amplitude')
        plt.show()
           
        plt.subplot(222)
        plt.plot(np.abs(X_H),'ro-')
        plt.title('X*H')
        plt.show()
        
        plt.subplot(223)
        plt.plot(np.abs(No),'yo-')
        plt.title('No(SNR=%s)'%(SNR[j]))
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.show()
        
        plt.subplot(224)
        plt.plot(np.abs(Y),'go-')
        plt.title('Y=X*H+No')
        plt.xlabel('Frequency')
        plt.show()
        
    return (cs_mse_ave,ls_mse_ave,mmse_mse_ave)