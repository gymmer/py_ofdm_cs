# -*- coding: utf-8 -*-

import numpy as np
from numpy import zeros,size,sqrt,sum
from numpy.random import randn

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

def awgn(X,SNR):
    ''' AWGN信道传输模型 '''
    SNR_log=10**(SNR/10.0)
    xpower=sum(X**2)/len(X)
    npower=xpower/SNR_log
    No=randn(len(X)) * sqrt(npower)
    Y = zeros(X.shape,X.dtype)
    for i in range(len(X)):
        Y[i]=X[i]+No[i]
    return Y

def how_many_equal(arrA,arrB):
    ''' 求两个数组中，相同元素的个数 '''
    equal = 0    
    for pos in arrA:
        if pos in arrB:
            equal += 1
    return equal