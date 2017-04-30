# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 23:10:34 2016

@author: gymmer
"""

import numpy as np
import math
from numpy import dot,mean,eye,transpose,conjugate,diag,real,zeros
from numpy.linalg import inv
from math import pi,e

def fftMatrix(N,L):
    W = np.zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            W[n,l] = e**(-1j*2*pi*n*l/N)
    W = 1/math.sqrt(N)*W
    return W

def MSE_SER_calc(H,re_H,X,Y,N):
    ''' calculate MSE and SER '''
    
    ''' MSE '''
    abs_diff = np.abs(H-re_H)/np.abs(H)
    MSE_mat = mean(abs_diff**2,1)
    
    for i in range(N):
        if MSE_mat[i]!=0:
            MSE = MSE_mat[i]
    
    ''' SER '''
    # re_X代表判决矩阵,根据接收到的信号Y和信道估计量re_H,反推导出观测矩阵的估计量re_X 
    # 由re_H=X'*Y 得到 re_X=re_H'*Y 
    # 即估计出观测矩阵re_X，用估计的发送信号re_X与实际发送的信号X比较，判断误码
    err_num = 0
    re_H_diag = zeros((N,N),dtype=np.complex)
    for i in range(N):
        re_H_diag[i,i] = re_H[i,0]
    re_X = dot(inv(re_H_diag),Y)
    
    # 得到观测矩阵的估计量
    for k in range(N): 
        if real(re_X[k])>0:
            re_X[k] = 1
        else:
            re_X[k] = -1
   
    # 与原信号比较计算误符号数 
    Xn = diag(X)
    for k in range(N): 
        if re_X[k]!=Xn[k]:
            err_num = err_num+1
    SER = err_num/N
    
    ''' return '''
    return (MSE,SER)
 
def LS_calc(X,H,Y,N):

    ''' 计算 LS 信道估计量 H_ls,返回MSE、SER '''
    
    H_ls = dot(inv(X),Y)
    return MSE_SER_calc(H,H_ls,X,Y,N)
    
def MMSE_calc(X,H,Y,Rgg,variance,N,L):
        
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
    
    return MSE_SER_calc(H,H_mmse,X,Y,N)