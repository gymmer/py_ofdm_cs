# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:36:21 2016

@author: gymmer
"""
import numpy as np

from numpy import dot,mean
from numpy.linalg import inv


def LS_MSE_calc(X,H,Y,N):

    '''
    This function generates mean squared error for the the LS estimator
    EVALUATION OF Hls
    The simplest of 'em all indeed..
    '''

    Hls = dot(inv(X),Y)
    abs_diff = np.abs(H-Hls)/np.abs(H)
    ms_error_mat = mean(abs_diff**2,1)
    
    for i in range(N):
        if ms_error_mat[i]!=0:
            ms_error = ms_error_mat[i]
    return ms_error