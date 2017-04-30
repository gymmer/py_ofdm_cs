# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:07:45 2016

@author: gymmer
"""

import numpy as np
import math
from numpy import mean,zeros,size
from math import pi,e

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
    
def MSE(H,re_H):
    ''' calculate MSE '''
    MSE = mean(abs(H-re_H)**2,0)    # 常规计算
    MSE = MSE / mean(abs(H**2),0)   # 归一化
    MSE = 10*math.log10(MSE)        # 取dB
    return MSE

def BMR(bitA,bitB):
    diff = np.abs(bitA-bitB)
    BMR = np.sum(diff)/(size(bitA)+0.0)
    return BMR
    
def interpolation(Hp,pos,N):
    
    ''' 插值 
    Hp:  导频处的信道频率响应
    Pos: 导频符号的位置
    N:   子载波数/插值后信道频率响应的长度
    '''
    P = size(pos)  
    H = zeros(N,dtype=np.complex)                 # 插值后的信道频率响应
    # 对导频符号进行线性插值
    for i in range(P-1):
        start = Hp[i]
        end   = Hp[i+1]
        inter = pos[i+1]-pos[i]
        step  = (end-start)/inter
        for j in range(inter):
            H[pos[i]+j] = Hp[i]+j*step
    H[pos[P-1]] = Hp[P-1]    
    # 对于第一个导频之前，和最后一个导频之后，进行常数插值。
    # 其数值分别等于第一个或最后一个导频的值
    for i in range(pos[0]):
        H[i]=Hp[0]
    for i in range(pos[P-1]+1,N):
        H[i]=Hp[P-1]
    return H