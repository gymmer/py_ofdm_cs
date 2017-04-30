# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:29:28 2016

@author: gymmer
"""

import random
from numpy import dot,eye
from OMP import OMP

def receiver_eva(Y,W,N,K,P):
    
    ''' 假设非法用户用另一个导频图样进行解码 '''
    ''' 非法用户猜测的导频位置 '''
    pos_eva = random.sample(range(N),P)     # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
    pos_eva.sort()
    
    ''' 导频选择矩阵 '''
    I = eye(N,N)                # NxN的单位矩阵
    S_eva  = I[pos_eva,:]       # PxN的导频选择矩阵
    
    ''' 提取导频 '''
    Yp_eva = dot(S_eva,Y)       # Px1的导频位置的接受信号向量
    Xp_eva = eye(P,P)           # 非法用户不知道X,但他知道，如果导频位置设为1，Xp实际上就是PxP的单位矩阵
    Wp_eva = dot(S_eva,W)       # PxL的矩阵,从W中选取与导频位置对应的P行
    
    
    ''' CS信道估计 '''
    h_eva = OMP(K,Yp_eva,Xp_eva,Wp_eva)
    H_eva = dot(W,h_eva)
        
    return h_eva,H_eva