# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:04:31 2016

@author: My402
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import size,dot,mean,diag,zeros,transpose,var,conjugate
from numpy.random import randn,randint
from OMP import OMP
from function import awgn,fftMatrix,ifftMatrix,MSE_SER_calc
from LS_MMSE import LS,MMSE
        

    
def channelEstimation(K,h,SNR,N):
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
    # 假设采用BPSK调制，符号为+1/-1
    #Xn = randint(low=0,high=2,size=N)*2-1
        
    ''' 测量矩阵 '''
    # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
    X = diag(Xn)
        
    ''' 求h的自协方差矩阵 '''
    gg = diag(h)
    
    gg_myu = np.sum(gg,0)/L
    gg_myu.shape = (L,1)
    gg_myu_t = conjugate(transpose(gg_myu))
    
    gg_myu_expend = gg_myu_t   # gg_myu是一个1xL行向量，gg_myu_expend是一个LxL矩阵，其每一行都是gg_myu
    for i in range(L-1):
        gg_myu_expend = np.r_[gg_myu_expend,gg_myu_t]
        
    gg_mid   = gg-gg_myu_expend
    gg_mid_t = conjugate(transpose(gg_mid))
    
    sum_gg_mid = np.sum(gg_mid,0);  # 每一列的值求和得1*L的矩阵
    sum_gg_mid.shape = (1,L)
    sum_gg_mid_t = conjugate(transpose(sum_gg_mid))
    
    Rgg = (dot(gg_mid_t,gg_mid) - dot(sum_gg_mid_t,sum_gg_mid)/L) / (L-1)  # Rgg是信道自协方差矩阵
    
    ''' 信道估计, 计算MSE、SER并作图比较CS、LS和MMSE '''
    CS_MSE   = zeros((group_num,SNR_num))
    CS_SER   = zeros((group_num,SNR_num))
    LS_MSE   = zeros((group_num,SNR_num))
    LS_SER   = zeros((group_num,SNR_num))
    MMSE_MSE = zeros((group_num,SNR_num))
    MMSE_SER = zeros((group_num,SNR_num))
    
    for i in range(group_num):          # 多组实验取平均
        for j in range(SNR_num):        # 比较不同的信噪比
        
            ''' 添加高斯白噪声，得接收信号向量Y '''
            X_H = dot(X,H);             # 理想信道传输,X_H = X*H
            Y = awgn(X_H,SNR[j])        # 加入复高斯白噪声,得到接收到的信号（频域表示）
            No = Y-X_H                  # Y = X*H + No
            var_No = var(No);           # 计算噪声方差
            
            ''' CS信道估计H，得MSE'''
            # s   = Phi*Psi*x
            # Y   = X  * W *h + N
            #     = X  * H    + N
            # hat_H = omp(K,s,Phi,Psi)
            #   ==>   s   = Y;  
            #   ==>   Phi = X;
            #   ==>   Psi = W;                       
            H_cs = OMP(K,Y,X,W)
                        
            ''' LS信道估计 '''
            H_ls = LS(X,H,Y,N)
                       
            ''' MMSE信道估计 '''
            H_mmse = MMSE(X,H,Y,Rgg,var_No,N,L)
            
            ''' 计算MSE、SER '''
            (CS_MSE[i,j],CS_SER[i,j]) = MSE_SER_calc(H,H_cs,X,Y,N)
            (LS_MSE[i,j],LS_SER[i,j]) = MSE_SER_calc(H,H_ls,X,Y,N)
            (MMSE_MSE[i,j],MMSE_SER[i,j]) = MSE_SER_calc(H,H_mmse,X,Y,N)
    
    CS_MSE_ave   = mean(CS_MSE,0)
    CS_SER_ave   = mean(CS_SER,0)
    LS_MSE_ave   = mean(LS_MSE,0)
    LS_SER_ave   = mean(LS_SER,0)
    MMSE_MSE_ave = mean(MMSE_MSE,0)
    MMSE_SER_ave = mean(MMSE_SER,0)
          
    ''' 画图 '''
    if N==128:
        ''' 假设非法用户用另一个测量矩阵X进行解码 '''
        X_invalid = diag(randn(N))
        re_H_invalid = OMP(K,Y,X_invalid,W)
        re_H = H_cs
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
        plt.title('Reconstruct h after Channel Estimation')
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
        plt.title('Reconstruct H after Channel Estimation')
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
        
    return (CS_MSE_ave,CS_SER_ave,LS_MSE_ave,LS_SER_ave,MMSE_MSE_ave,MMSE_SER_ave)