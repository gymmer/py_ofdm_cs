# -*- coding: utf-8 -*-

import sys
from numpy import dot,transpose,eye,size
from numpy.linalg import inv
from numpy.fft import fft
from default import *

sys.path.append('../')
from util.mathematics import fftMatrix,ifftMatrix
from util.function import guess_pos
from PHY import OMP,remove_OFDM_pilot,diagram_demod,normal_coef,interlace_decode,viterbi_decode,interpolation

def receiver(y,pos,etype=detype,pos_type=dpos_type,L=dL,K=dK,N=dN,Ncp=dNcp,modulate=dmodulate):
    '''
    y:        接收信号
    pos:      导频图样
    etype:    'CS' 或 'LS'
    pos_type: 'from_pos'：使用传入的参数 pos 作为导频图样
              其他（数字类型）：与 pos 相比，猜对了其中【数字】个导频位置。用于：非法用户随机猜测导频位置，此时传入的pos为发送端的导频图样
    L:        信道长度
    K:        稀疏度
    N:        子载波数
    Ncp:      循环前缀长度
    modulate: 星座调制
    '''
    
    P = size(pos)
    if pos_type != 'from_pos':
        right_num = int(pos_type)
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
    I = eye(N,N)                        # NxN的单位矩阵
    S = I[pos,:]                        # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
    ''' 提取导频 ''' 
    Yp = dot(S,Y)                       # Px1的导频位置的接受信号向量
    #Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
    Xp = eye(P,P)    
    W = fftMatrix(N,L)                  # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基      
    Wp = dot(S,W)                       # PxL的矩阵,从W中选取与导频位置对应的P行
    
    if etype=='CS':
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
        re_h = OMP(K,Yp,Xp,Wp)              # OMP是时域估计算法，估计得到时域的h
        re_H = dot(W,re_h)                  # 傅里叶变换，得到频域的H
    elif etype=='LS':       
        ''' LS信道估计 '''
        Hp_ls = dot(inv(Xp),Yp)             # LS、MMSE是频域估计算法，得到导频处的Hp
        re_H = interpolation(Hp_ls,pos,N)   # 根据导频处Hp进行插值，恢复信道的H     
        re_h = dot(ifftMatrix(L,N),re_H)    # 傅里叶逆变换，得到时域的h
    
    ''' 信道均衡 '''
    Y = Y/re_H
    
    ''' 移除导频 '''   
    Y = remove_OFDM_pilot(Y,pos)
    
    ''' 星座点归一化 '''
    diagram = Y*normal_coef[modulate]
    
    ''' BPSK/QPSK/16QAM解调 '''
    bits = diagram_demod(diagram,modulate)

    ''' 解交织 '''
    bits = interlace_decode(bits,2,size(bits)/2)
    
    ''' viterbi译码 '''
    bits = viterbi_decode(bits)
    
    return re_h,re_H,bits,diagram