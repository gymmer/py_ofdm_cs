# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:07:45 2016

@author: gymmer
"""

import numpy as np
import math
from numpy import mean
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