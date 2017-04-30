# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:06:33 2016

@author: My402
"""

import numpy as np
from numpy import dot,transpose,eye,size
from numpy.linalg import inv
from numpy.fft import fft
from OMP import OMP
from function import ifftMatrix,interpolation
import QAM16

def receiver(y,W,L,N,Ncp,K,pos,etype):
    
    ''' 移除循环前缀'''
    y = y[:,Ncp:]
    
    ''' 串并转换 '''
    y = y.reshape(N,1)
    
    ''' FFT '''
    Y = fft(y,axis=0)

    ''' 并串转换 '''
    pass

    ''' 导频选择矩阵 '''
    P = size(pos)
    I = eye(N,N)    # NxN的单位矩阵
    S = I[pos,:]    # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
    ''' 提取导频 ''' 
    Yp = dot(S,Y)                       # Px1的导频位置的接受信号向量
    #Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
    Xp = eye(P,P)    
    Wp = dot(S,W)                       # PxL的矩阵,从W中选取与导频位置对应的P行
    
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
        re_h = OMP(K,Yp,Xp,Wp)      # OMP是时域估计算法，估计得到时域的h
        re_H = dot(W,re_h)          # 傅里叶变换，得到频域的H
    elif etype=='LS':       
        ''' LS信道估计 '''
        Hp_ls = dot(inv(Xp),Yp)             # LS、MMSE是频域估计算法，得到导频处的Hp
        re_H = interpolation(Hp_ls,pos,N)   # 根据导频处Hp进行插值，恢复信道的H     
        re_h = dot(ifftMatrix(L,N),re_H)    # 傅里叶逆变换，得到时域的h
    
    ''' 信道均衡 '''
    Y = Y/re_H

    ''' 16-QAM解调 '''
    bits = QAM16.demod(Y)
    
    return re_h,re_H,bits