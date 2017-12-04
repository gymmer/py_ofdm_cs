# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import dot,transpose,eye,size,zeros,real,imag
from numpy.linalg import inv
from numpy.fft import fft

sys.path.append('../')
from util.mathematics import fftMatrix,ifftMatrix
from util.function import guess_pos
from PHY import OMP,remove_MIMO_pilot,diagram_demod,normal_coef,interlace_decode,viterbi_decode,STBC_decode,interpolation

def receiver(y,L,K,N,M,Ncp,Nt,Nr,pos,demodulate_type,etype="CS",pos_type="from_pos"):
    
    '''
    y: 接收信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    Nt: 发送天线数
    Nr: 接收天线数
    pos: 导频图样
    demodulate_type: 调制方式。1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
    etype: 'CS' 或 'LS'
    pos_type：
        'from_pos'：使用传入的参数 pos 作为导频图样
        其他（数字类型）：与 pos 相比，猜对了其中【数字】个导频位置。用于：非法用户随机猜测导频位置，此时传入的pos为发送端的导频图样
    '''
    
    P = size(pos)
    if pos_type != 'from_pos':
        right_num = int(pos_type)
        pos = guess_pos(N,P,pos,right_num)

    ''' CS/LS重构的信道响应 '''
    re_h = zeros((Nr,Nt,L,M),dtype=np.complex)
    re_H = zeros((Nr,Nt,N,M),dtype=np.complex)
    
    ''' 接收天线接收的数据'''
    Y = zeros((N,M,Nr),dtype=np.complex) # N*M*Nr,利用第三维表示不同天线接收的OFDM符号
    
    for r in range(Nr):

        ''' 第r个天线的接收数据 '''
        y_r = y[:,r]
        
        ''' 串并转换 '''
        y_r = y_r.reshape(-1,M)
        
        ''' 移除循环前缀'''
        y_r = y_r[Ncp:,:]
            
        ''' FFT '''
        Y_r = fft(y_r,axis=0)
        Y[:,:,r] = Y_r
        
        ''' 估计第t个发送天线与第r个发送天线之间的h_rt'''   
        for t in range(Nt):
            
            ''' 第t个天线上的导频图样'''
            pos_t = pos[:,t]
            
            ''' 导频选择矩阵 '''
            P = size(pos_t)
            I = eye(N,N)                # NxN的单位矩阵
            S = I[pos_t,:]              # PxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的P行，用于从N个子载波中选择出P个导频位置
    
            ''' 提取导频 ''' 
            Yp = dot(S,Y_r)             # Px1的导频位置的接受信号向量
            #Xp = dot( dot(S,X), transpose(S) ) # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
            Xp = eye(P,P)
            W = fftMatrix(N,L)          # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基  
            Wp = dot(S,W)               # PxL的矩阵,从W中选取与导频位置对应的P行
    
            if etype=='CS':
                ''' CS信道估计'''            
                # X_wave作为密钥。若Xp是单位矩阵，则Xp*Wp=Wp，密钥取决于Wp。
                # 而Wp又是从W中选取的与导频位置对应的P行，所以密钥取决于导频位置pos
                for m in range(M):                                      # 第m个符号的CS重构的h。对于慢衰落信道，不同符号的重构h应该大致相同
                    re_h[r,t,:,m] = OMP(K,Yp[:,m],Xp,Wp).reshape(L)     # OMP是时域估计算法，估计得到时域的h                                  
                    re_H[r,t,:,m] = dot(W,re_h[r,t,:,m])                # 傅里叶变换，得到频域的H
                
            elif etype=='LS':       
                ''' LS信道估计 '''
                Hp_ls = dot(inv(Xp),Yp)                                 # LS、MMSE是频域估计算法，得到导频处的Hp
                for m in range(M):                                      # 对第m个符号的Hp进行插值
                    re_H[r,t,:,m] = interpolation(Hp_ls[:,m],pos_t,N)   # 根据导频处Hp进行插值，恢复信道的H             
                    re_h[r,t,:,m] = dot(ifftMatrix(L,N),re_H[r,t,:,m])  # 傅里叶逆变换，得到时域的h        
    
    ''' 空时解码 '''
    Y = STBC_decode(Y,re_H,N,M,Nt,Nr)

    ''' 移除导频 '''   
    Y = remove_MIMO_pilot(Y,pos)
    
    ''' 并串转换 '''
    diagram = Y.reshape(-1)
    
    ''' 星座点归一化 '''
    diagram = diagram*normal_coef[demodulate_type]
    
    ''' BPSK/QPSK/16QAM解调 '''
    bits = diagram_demod(diagram,demodulate_type)

    ''' 解交织 '''
    bits = interlace_decode(bits,8,size(bits)/8)
    
    ''' viterbi译码 '''
    bits = viterbi_decode(bits)
    
    return re_h,re_H,bits,diagram