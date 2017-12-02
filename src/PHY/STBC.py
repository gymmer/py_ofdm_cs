# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 09:38:55 2016

@author: My402
"""

import numpy as np
from numpy import zeros,conj

def Alamouti(toBe_code,N):
    '''
    toBe_code: 待编码的发送信号
    N：载波数
    '''      
    Xe = toBe_code[:,0]     #取第一列，即第一个OFDM符号
    Xo = toBe_code[:,1]     #取第二列，即第二个OFDM符号
    
    coded = np.zeros((N,2,2),dtype=np.complex)
    coded[:,0,0] = Xe
    coded[:,0,1] = Xo
    coded[:,1,0] = -conj(Xo)
    coded[:,1,1] = conj(Xe)
    return coded

def decode_Tx2_Rx2(H,toBe_decode,N):
    ''' 
    H：频域信道矩阵，Nr*Nt*N*M
    toBe_decode: 待解码的接收信号，共2个OFDM符号。N*2*Nr
    N：载波数
    '''
    
    ''' 各收发天线的信道参数 '''
    # 对于慢衰落信道，假设多个OFDM符号内的信道响应不变，所以只取第一个符号
    H11 = H[0,0,:,0]            # 第一个发送天线，与第一个接收天线的信道参数
    H12 = H[1,0,:,0]            # 第一个发送天线，与第二个接收天线的信道参数
    H21 = H[0,1,:,0]            # 第二个发送天线，与第一个接收天线的信道参数
    H22 = H[1,1,:,0]            # 第二个发送天线，与第二个接收天线的信道参数
    
    ''' 各接收天线收到的OFDM符号 '''
    R11 = toBe_decode[:,0,0]    # 第一个接收天线，接收到的第一个符号
    R12 = toBe_decode[:,1,0]    # 第一个接收天线，接收到的第二个符号
    R21 = toBe_decode[:,0,1]    # 第二个接收天线，接收到的第一个符号
    R22 = toBe_decode[:,1,1]    # 第二个接收天线，接收到的第二个符号
    
    ''' 合并后的OFDM符号 '''
    temp1 = R11*conj(H11) + conj(R12)*H21 + R21*conj(H12) + conj(R22)*H22
    temp2 = R11*conj(H21) - conj(R12)*H11 + R21*conj(H22) - conj(R22)*H12
    temp3 = H11*conj(H11) + conj(H12)*H12 + H21*conj(H21) + conj(H22)*H22
    Xe = temp1/temp3
    Xo = temp2/temp3
    return np.c_[Xe.reshape(N,1),Xo.reshape(N,1)]

def ML_detection(point):
    diagram = np.array([-3-3j,-3-1j,-3+1j,-3+3j,-1-3j,-1-1j,-1+1j,-1+3j,1-3j,1-1j,1+1j,1+3j,3-3j,3-1j,3+1j,3+3j])
    d = np.zeros(16)
    for i in range(16):
        d[i] = np.abs( point-diagram[i] )**2
    index = np.argmin(d)
    return diagram[index]
    
def decode_Tx2_Rx1(H,toBe_decode,N):
    ''' 
    H：频域信道矩阵，Nr*Nt*N*M
    toBe_decode: 待解码的接收信号，共2个OFDM符号。N*2*Nr
    N：载波数
    '''
    
    ''' 各收发天线的信道参数 '''
    # 对于慢衰落信道，假设多个OFDM符号内的信道响应不变，所以只取第一个符号
    H1 = H[0,0,:,0]             # 第一个发送天线，与接收天线的信道参数
    H2 = H[0,1,:,0]             # 第二个发送天线，与接收天线的信道参数
    
    ''' 各接收天线收到的OFDM符号 '''
    R1 = toBe_decode[:,0,0]     # 接收天线的第一个符号
    R2 = toBe_decode[:,1,0]     # 接收天线的第二个符号
    
    ''' 合并后的OFDM符号 '''      
    temp1 = R1*conj(H1) + conj(R2)*H2
    temp2 = R1*conj(H2) - conj(R2)*H1
    temp3 = H1*conj(H1) + conj(H2)*H2
    Xe = temp1/temp3
    Xo = temp2/temp3
    return np.c_[Xe.reshape(N,1),Xo.reshape(N,1)]

def STBC_code(symbol,N,M,Nt):
    '''
    symbol：发射天线待编码的所有OFDM符号，N*M
    N：载波数
    M：符号数
    Nt：发送天线数
    '''
    MIMO = zeros((N,M,Nt),dtype=np.complex)
    
    if Nt==1:
        ''' 只有1个发射天线 '''
        MIMO = symbol.reshape(N,M,1)
        
    elif Nt==2:
        ''' 2个发射天线 '''       
        for i in range(M/Nt):
            # 一次送入空时编码器的OFDM符号有Nt个，如发送天线为2，则一次送入两个OFDM符号进行Alamouti编码
            toBe_code = symbol[:,i*Nt:(i+1)*Nt]
            # coded的结构: N*2*2.有N行,代表不同时间OFDM符号的M列,矩阵第三维为Nt个,代表不同天线的数据
            coded = Alamouti(toBe_code,N)
            MIMO[:,i*Nt:(i+1)*Nt,:] = coded
    return MIMO

def STBC_decode(symbol,H,N,M,Nt,Nr):
    '''
    symbol: 接收天线待解码的所有OFDM符号，N*M*Nr
    H：频域信道矩阵，Nr*Nt*N*M  
    N：载波数
    M：符号数
    Nt：发送天线数
    Nr：接收天线数
    '''
    SISO = zeros((N,M),dtype=np.complex)
    
    if Nt==1 and Nr==1:
        ''' 信道均衡 '''
        SISO = symbol[:,:,0]/H[0,0,:,:] 
        
    elif Nt==2:
        for i in range(M/Nt):
            # 一次送入空时解码器的OFDM符号有Nt个，如发送天线为2，则一次送入两个OFDM符号进行解码
            toBe_decode = symbol[:,i*Nt:(i+1)*Nt,:]
            if Nr==1:
                decoded = decode_Tx2_Rx1(H,toBe_decode,N)
            elif Nr==2:
                decoded = decode_Tx2_Rx2(H,toBe_decode,N)
            SISO[:,i*Nt:(i+1)*Nt] = decoded
    return SISO
