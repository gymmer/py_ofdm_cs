# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:04:31 2016

@author: My402
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from numpy import size,dot,mean,diag,zeros,transpose,var,conjugate,eye
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
        
    ''' 导频数 ''' 
    P = 6*K  # 导频数
    ND = N-P # 数据载波数 
    pos = random.sample(range(N),P)    # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
    pos.sort()
    
    ''' 插入导频,导频位置设为1 '''
    Xn[pos] = 1
    
    ''' 测量矩阵 '''
    # 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
    X = diag(Xn)
    
    
    I = eye(N,N)    # NxN的单位矩阵
    S = I[pos,:]    # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
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
            
            ''' 插入导频 ''' 
            Yp = dot(S,Y)                       # Px1的导频位置的接受信号向量
            Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
            Wp = dot(S,W)                       # PxL的矩阵,从W中选取与导频位置对应的P行
            Np = dot(S,No)                      # 噪声向量
            
            ''' CS信道估计H，得MSE'''
            # s   = Phi*Psi*x
            # Y   = X  * W *h + N
            #     = X  * H    + N
            # hat_H = omp(K,s,Phi,Psi)
            #   ==>   s   = Y;  
            #   ==>   Phi = X;
            #   ==>   Psi = W;  
            # Xp*Wp作为密钥。若Xp是单位矩阵，则Xp*Wp=Wp，密钥取决于Wp。
            # 而Wp又是从W中选取的与导频位置对应的P行，所以密钥取决于导频位置pos
            h_cs = OMP(K,Yp,Xp,Wp)      # OMP是时域估计算法，估计得到时域的h
            H_cs = dot(W,h_cs)          # 傅里叶变换，得到频域的H
                        
            ''' LS信道估计 '''
            H_ls = LS(X,Y)          # LS、MMSE是频域估计算法，估计得到频域的H
            h_ls = dot(ifftMatrix(L,N),H_ls)    # 傅里叶逆变换，得到时域的h
                       
            ''' MMSE信道估计 '''
            H_mmse = MMSE(X,H,Y,Rgg,var_No,N,L)
            h_mmse = dot(ifftMatrix(L,N),H_mmse)
            
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
    ''' 假设非法用户用另一个导频图样进行解码 '''
    pos_invalid = random.sample(range(N),P)     # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
    pos_invalid.sort()
    I = eye(N,N)                                # NxN的单位矩阵
    S_invalid  = I[pos_invalid,:]               # PxN的导频选择矩阵
    Yp_invalid = dot(S_invalid,Y)               # Px1的导频位置的接受信号向量
    Xp_invalid = eye(P,P)                       # 非法用户不知道X,但他知道，如果导频位置设为1，Xp实际上就是PxP的单位矩阵
    Wp_invalid = dot(S_invalid,W)
    re_h_invalid = OMP(K,Yp_invalid,Xp_invalid,Wp_invalid)
    re_H_invalid = dot(W,re_h_invalid)
    
    ''' 信道估计得到的h、H'''
    re_h = h_cs
    re_H = H_cs

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