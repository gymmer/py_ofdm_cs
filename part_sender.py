# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

from numpy.random import randn

def sender (N,P,pos):
    
    ''' 发送端序列的频谱Xn '''
    Xn = randn(N)           # 均值为0，方差为1的正态分布
 
    ''' 插入导频,导频位置设为1 '''
    Xn[pos] = 1
    
    return Xn