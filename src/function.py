# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:07:45 2016

@author: gymmer
"""

import numpy as np
import math
import operator
from numpy import mean,zeros,size
from math import pi,e,log

def fac(n):
    ''' 计算阶乘 '''
    if n==0:
        return 1
    else:
        return reduce(operator.mul,range(1,n+1)) 
        
def c(n,m):
    ''' 计算组合数 '''
    return fac(n)/(fac(m)*fac(n-m))

def fftMatrix(N,L):
    W = zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            W[n,l] = e**(-1j*2*pi*n*l/N)
    W = 1/math.sqrt(N)*W
    return W
    
def ifftMatrix(N,L):
    w = zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            w[n,l] = e**(1j*2*pi*n*l/L)
    w = 1/math.sqrt(L)*w
    return w
    
def MSE(H,re_H):
    ''' 求MSE '''
    MSE = mean(abs(H-re_H)**2,0)    # 常规计算
    MSE = MSE / mean(abs(H**2),0)   # 归一化
    MSE = 10*math.log10(MSE)        # 取dB
    return MSE

def BMR(bits_A,bits_B):
    diff = np.abs(bits_A-bits_B)
    BMR = np.sum(diff)/(size(bits_A)+0.0)
    return BMR

def BGR(bits,sampling_time,sampling_period):
    ''' 求BGR '''
    BGR = size(bits)/(sampling_time*1000.0/sampling_period)
    return BGR

def entropy(p):
    ''' 求信息熵 '''
    if p==0 or p==1:
        return 0
    else:
        return -p*log(p,2)-(1-p)*log(1-p,2)
        
def SecCap(BER_B,BER_E):
    ''' 求安全容量 '''
    return entropy(BER_E) - entropy(BER_B)
    
def interpolation(Hp,pos,N):
    
    ''' 插值 
    Hp:  导频处的信道频率响应
    Pos: 导频符号的位置
    N:   子载波数/插值后信道频率响应的长度
    '''
    P = size(pos)  
    H = zeros((N,1),dtype=np.complex)                 # 插值后的信道频率响应
    # 对导频符号进行线性插值
    for i in range(P-1):
        start = Hp[i,0]
        end   = Hp[i+1,0]
        inter = pos[i+1]-pos[i]
        step  = (end-start)/inter
        for j in range(inter):
            H[pos[i]+j,0] = Hp[i,0]+j*step
    H[pos[P-1]] = Hp[P-1]    
    # 对于第一个导频之前，和最后一个导频之后，进行常数插值。
    # 其数值分别等于第一个或最后一个导频的值
    for i in range(pos[0]):
        H[i,0]=Hp[0,0]
    for i in range(pos[P-1]+1,N):
        H[i,0]=Hp[P-1,0]
    return H

def how_many_equal(arrA,arrB):
    ''' 求两个数组中，相同元素的个数 '''
    equal = 0    
    for pos in arrA:
        if pos in arrB:
            equal += 1
    return equal