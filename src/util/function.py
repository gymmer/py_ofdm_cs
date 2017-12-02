# -*- coding: utf-8 -*-

from numpy import zeros,sqrt,sum
from numpy.random import randn

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