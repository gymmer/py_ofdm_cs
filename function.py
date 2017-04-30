# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:07:45 2016

@author: gymmer
"""

import numpy as np
import math
from numpy import dot,mean,diag,real,zeros
from numpy.linalg import inv
from numpy.random import randn
from math import pi,e

def awgn(X,SNR):
    SNR_log=10**(SNR/10.0)
    xpower=np.sum(X**2)/len(X)
    npower=xpower/SNR_log
    No=randn(len(X)) * np.sqrt(npower)
    Y = np.zeros(X.shape,X.dtype)
    for i in range(len(X)):
        Y[i]=X[i]+No[i]
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
    
def MSE_SER_calc(H,re_H,X,Y,N):
    ''' calculate MSE and SER '''
    
    ''' MSE '''
    MSE = mean(abs(H-re_H)**2,0)
    
    ''' SER '''
    # re_X代表判决矩阵,根据接收到的信号Y和信道估计量re_H,反推导出观测矩阵的估计量re_X 
    # 由re_H=X'*Y 得到 re_X=re_H'*Y 
    # 即估计出观测矩阵re_X，用估计的发送信号re_X与实际发送的信号X比较，判断误码
    err_num = 0.0
    ''' 这部分有问题，还需要继续修改。re_X=+1或-1，但是Xn不一定是+1或-1，比较二者没有意义
    应该是，时域+1或-1，频域X，恢复的re_X，再变回时域，根据正负判决为+1或-1，计算SER
    对于BPSK，是指其时域是+1、-1，而非频域
    re_H_diag = zeros((N,N),dtype=np.complex)
    for i in range(N):
        re_H_diag[i,i] = re_H[i,0]
    re_X = dot(inv(re_H_diag),Y)    # 得到频域估计量
    #re_x = np.fft.ifft(re_X)*N/2    # 得到时域估计量
    #print re_x
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
            err_num = err_num+1'''
    SER = err_num/N

    ''' return '''
    return (MSE,SER)