# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:05:04 2016

@author: My402
"""

from function import interpolation 
import numpy as np
import math
from numpy import mean,zeros,size,dot,diag,eye
from math import pi,e
from transmission import channel,awgn
from numpy.random import randn,seed
from function import fftMatrix
import random

seed(0)

N = 90
M = 20
L = 32
K = 6
PN = 24
PM = 5
SNR = 30
''' 发送端序列频谱 '''
Xn = randn(N,M)

''' 频域导频位置 '''    
posN = random.sample(range(N),PN)     # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
posN.sort()

''' 时域导频位置 '''
posM = random.sample(range(M),PM)     # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
posM.sort()

''' 插入导频,导频位置设为1 '''
for i in range(PM):
    Xn[posN,posM[i]] = 1

''' 信道冲激响应 '''
h = zeros((L,M),dtype = np.complex)
for i in range(M): # 一次产生各符号周期内的h
    h[:,i] = channel(L,K)

''' 信道频率响应H '''
W = fftMatrix(N,L)      # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基
H = zeros((N,M),dtype = np.complex)
for i in range(M):      # 每个符号周期内的H
    H[:,i] = dot(W,h[:,i]) # 频率的冲激响应
    
''' 测量矩阵 '''
# 将发送信号作为观测矩阵的对角元素,X=diag(X(0),X(1),...,X(N-1))是N*N的子载波矩阵
X = zeros((N,N,M),dtype = np.complex)
for i in range(M):
    X[:,:,i] = diag(Xn[:,i])

''' 理想信道传输 '''
X_H = zeros((N,M),dtype = np.complex)
for i in range(M):      # 每个符号周期内的H
    X_H[:,i] = dot(X[:,:,i],H[:,i]) # 频率的冲激响应

''' 添加高斯白噪声，得接收信号向量Y '''
Y = awgn(X_H,SNR)        # 加入复高斯白噪声,得到接收到的信号（频域表示）
No = Y-X_H               # Y = X*H + No

''' 频域导频选择矩阵 '''
I = eye(N,N)    # NxN的单位矩阵
SN = I[posN,:]    # PNxN的导频选择矩阵，从NxN的单位矩阵选取与导频位置对应的PN行，用于从N个子载波中选择出PN个导频位置

''' 时域导频选择矩阵 '''
I = eye(M,M)    # NxN的单位矩阵
SM = I[:,posM]    # MxPM的导频选择矩阵，从MxM的单位矩阵选取与导频位置对应的PM列，用于从M个OFDM符号中选择出PM个导频位置

''' 提取导频 ''' 
Yp = dot( dot(SN,Y),SM)                       # PNxPM的导频位置的接受信号向量
#Xp = dot( dot(S,X), transpose(S) )  # PxP的斜对角阵，对角线元素是导频位置的X。如果导频位置设为1，则Xp实际上就是PxP的单位矩阵
#Wp = dot( dot(SN,W),SM)                       # PxL的矩阵,从W中选取与导频位置对应的P行