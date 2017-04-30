# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 23:10:34 2016

@author: gymmer
"""

import numpy as np
import math
from numpy import dot,mean,eye,transpose,conjugate
from numpy.linalg import inv
from math import pi,e

def fftMatrix(N,L):
    W = np.zeros((N,L),dtype=np.complex)
    for n in range(N):
        for l in range(L):
            W[n,l] = e**(-1j*2*pi*n*l/N)
    W = 1/math.sqrt(N)*W
    return W
    
def MMSE_MSE_calc(X,H,Y,Rgg,variance,N,L):
    
    '''
    This function generates mean squared error for the the MMSE estimator
    EVALUATION OF Hmmse
    Hmmse=F*Rgg*inv(Rgy)*Y
    '''
    
    F = math.sqrt(N)*fftMatrix(N,L)
    I = eye(N)
    F_tr = conjugate(transpose(F))
    X_tr = conjugate(transpose(X))
    
    Rgy = dot( dot(Rgg,F_tr),X_tr )
    R1 = dot(dot(X,F),Rgg)
    Ryy = dot(dot(R1,F_tr),X_tr) + dot(variance,I)

    Gmmse = dot( dot(Rgy,inv(Ryy)), Y)
    Hmmse = dot(F,Gmmse)
    
    abs_diff = np.abs(H-Hmmse)/np.abs(H)
    ms_error_mat = mean(abs_diff**2,1)
    
    for i in range(N):
        if ms_error_mat[i]!=0:
            ms_error = ms_error_mat[i]
    return ms_error