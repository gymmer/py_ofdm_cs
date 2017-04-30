# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 23:10:34 2016

@author: gymmer
"""

import math
from numpy import dot,eye,transpose,conjugate
from numpy.linalg import inv
from function import fftMatrix
 
def LS(X,Y):

    ''' 计算 LS 信道估计量 H_ls,返回MSE、SER '''
    
    H_ls = dot(inv(X),Y)
    return H_ls
    
def MMSE(X,H,Y,Rgg,variance,N,L):
        
    ''' 计算MMSE 信道估计量 H_mmse，返回MSE、SER '''
    
    F = math.sqrt(N)*fftMatrix(N,L)                 # DFT变换系数矩阵
    I = eye(N)
    F_tr = conjugate(transpose(F))
    X_tr = conjugate(transpose(X))
    
    Rgy = dot( dot(Rgg,F_tr),X_tr )
    R1 = dot(dot(X,F),Rgg)
    Ryy = dot(dot(R1,F_tr),X_tr) + dot(variance,I)  # Ryy是接收信号的自协方差矩阵

    h_mmse = dot( dot(Rgy,inv(Ryy)), Y)             # 时域MMSE估计的信道响应
    H_mmse = dot(F,h_mmse)                          # 频域MMSE估计的信道响应
    
    return H_mmse