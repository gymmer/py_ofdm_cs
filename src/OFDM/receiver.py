# -*- coding: utf-8 -*-

import sys
import numpy as np
import random
from numpy import dot,transpose,eye,size,array
from numpy.linalg import inv
from numpy.fft import fft
from numpy.random import randint

sys.path.append('../')
from util.mathematics import fftMatrix,ifftMatrix
from util.function import interpolation
from PHY import OMP,remove_pilot,diagram_demod,normal_coef,interlace_decode,viterbi_decode

def guess_pos(N,P,pos,right_num):
        
    pos_original = array(pos)                       # 合法用户的导频序列
    where_right = random.sample(range(P),right_num) # 猜对的导频，一共P个导频，从中猜对了right_num个
    
    pos_eva = array([],dtype=np.int32)              # 非法用户随机猜的导频序列，初始化为空
    pos_eva_size = 0                                # 非法导频序列的位置，初始化为0
    while pos_eva_size < P:                         # 先生成一个与合法导频序列完全不同的非法导频序列
        new_pos = randint(low=0,high=N)   # 随机产生一个新的非法导频位置，取值[0,N)
        if (new_pos not in pos) and (new_pos not in pos_eva) : # 新的非法位置，不在合法序列中，也不与已产生的任意非法位置重合
            pos_eva = np.r_[pos_eva,new_pos]        # 只要满足了上述条件，这个新产生的位置才有效，加入到非法导频序列中
            pos_eva_size += 1                       # 更新非法导频序列的长度
    
    pos_eva[where_right] = pos_original[where_right]# 对于那些猜对的位置，更正非法导频序列
    pos_eva.sort()
    return pos_eva

def receiver(y,L,K,N,Ncp,pos,demodulate_type,esti_type,pos_type):
    '''
    y: 接收信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    Ncp: 循环前缀长度
    pos: 导频图样
    etype: 'CS' 或 'LS'
    '''
    
    P = size(pos)
    
    ''' 假设非法用户用另一个导频图样进行解码 '''
    if pos_type=='from_pos':        # 使用传入的pos作为导频图样（RSSI量化得到，或均匀放置）       
        pos = pos
    else:                           # 非法用户随机猜测导频位置。此时传入的pos为发送端的导频图样
        right_num = int(pos_type)   # 与pos相比，非法用户猜对了right_num个
        pos = guess_pos(N,P,pos,right_num)
         
    ''' 移除循环前缀'''
    y = y[:,Ncp:]
    
    ''' 串并转换 '''
    y = y.reshape(N,1)
    
    ''' FFT '''
    Y = fft(y,axis=0)

    ''' 并串转换 '''
    pass

    ''' 导频选择矩阵 '''
    I = eye(N,N)    # NxN的单位矩阵
    S = I[pos,:]    # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
    ''' 提取导频 ''' 
    Yp = dot(S,Y)                       # Px1的导频位置的接受信号向量
    #Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
    Xp = eye(P,P)    
    W = fftMatrix(N,L)                  # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基      
    Wp = dot(S,W)                       # PxL的矩阵,从W中选取与导频位置对应的P行
    
    if esti_type=='CS':
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
        re_h = OMP(K,Yp,Xp,Wp)      # OMP是时域估计算法，估计得到时域的h
        re_H = dot(W,re_h)          # 傅里叶变换，得到频域的H
    elif esti_type=='LS':       
        ''' LS信道估计 '''
        Hp_ls = dot(inv(Xp),Yp)             # LS、MMSE是频域估计算法，得到导频处的Hp
        re_H = interpolation(Hp_ls,pos,N)   # 根据导频处Hp进行插值，恢复信道的H     
        re_h = dot(ifftMatrix(L,N),re_H)    # 傅里叶逆变换，得到时域的h
    
    ''' 信道均衡 '''
    Y = Y/re_H
    
    ''' 移除导频 '''   
    Y = remove_pilot(Y,pos)
    
    ''' 星座点归一化 '''
    diagram = Y*normal_coef[demodulate_type]
    
    ''' BPSK/QPSK/16QAM解调 '''
    bits = diagram_demod(diagram,demodulate_type)

    ''' 解交织 '''
    bits = interlace_decode(bits,2,size(bits)/2)
    
    ''' viterbi译码 '''
    bits = viterbi_decode(bits)
    
    return re_h,re_H,bits,diagram