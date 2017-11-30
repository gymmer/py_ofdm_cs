# -*- coding: utf-8 -*-

import numpy as np
import operator
from numpy import zeros
from math import pi,e,sqrt

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
    W = 1/sqrt(N)*W
    return W
    
def ifftMatrix(N,L):
    w = zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            w[n,l] = e**(1j*2*pi*n*l/L)
    w = 1/sqrt(L)*w
    return w