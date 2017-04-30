# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:06:33 2016

@author: My402
"""

import numpy as np
from numpy import dot,transpose,eye,arange
from numpy.linalg import inv
from OMP import OMP
from function import ifftMatrix,interpolation
from RSSI import sampling,quantization,hash_tiger
from RC4 import RC4

def receiver(Y,W,L,N,P,K,ptype,pos_sender):

    ''' 导频位置 '''
    if ptype=='random':     # 随机，根据RSSI生成导频位置
        ''' 导频位置应该从RSSI得到，但是RSSI部分尚未完善，导频误差很大。此处先临时用sender的导频图样
        应当保证sender的key和receiver的key完全一样
        RSSI = sampling(1,1,1)+np.random.randint(0,2,size=(1000,1))
        bit = quantization(RSSI,2,1)
        key = hash_tiger(bit)
        pos = RC4(key,P) 
        '''
        pos = pos_sender
    elif ptype == 'even':   # 均匀
        pos = arange(P)*5   # 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个

    ''' 导频选择矩阵 '''
    I = eye(N,N)    # NxN的单位矩阵
    S = I[pos,:]    # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
    ''' 提取导频 ''' 
    Yp = dot(S,Y)                       # Px1的导频位置的接受信号向量
    #Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
    Xp = eye(P,P)    
    Wp = dot(S,W)                       # PxL的矩阵,从W中选取与导频位置对应的P行
    
    ''' CS信道估计'''
    # s   = Phi*Psi*x
    # Y   = X  * W *h + N
    #     = X  * H    + N
    # hat_H = omp(K,s,Phi,Psi)
    #   ==>   s   = Y
    #   ==>   Phi = X
    #   ==>   Psi = W
    
    # Xp*Wp作为密钥。若Xp是单位矩阵，则Xp*Wp=Wp，密钥取决于Wp。
    # 而Wp又是从W中选取的与导频位置对应的P行，所以密钥取决于导频位置pos
    h_cs = OMP(K,Yp,Xp,Wp)      # OMP是时域估计算法，估计得到时域的h
    H_cs = dot(W,h_cs)          # 傅里叶变换，得到频域的H
           
    ''' LS信道估计 '''
    Hp_ls = dot(inv(Xp),Yp)             # LS、MMSE是频域估计算法，得到导频处的Hp    
    H_ls = interpolation(Hp_ls,pos,N)   # 根据导频处Hp进行插值，恢复信道的H     
    h_ls = dot(ifftMatrix(L,N),H_ls)    # 傅里叶逆变换，得到时域的h
        
    return h_cs,H_cs,h_ls,H_ls