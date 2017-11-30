# -*- coding: utf-8 -*-

from numpy import mean,size,abs,sum
from math import log,log10

def MSE(H,re_H):
    ''' 求MSE '''
    MSE = mean(abs(H-re_H)**2,0)    # 常规计算
    MSE = MSE / mean(abs(H**2),0)   # 归一化
    MSE = 10*log10(MSE)        # 取dB
    return MSE

def BMR(bits_A,bits_B):
    ''' 求比特错误率 '''
    diff = abs(bits_A-bits_B)
    BMR = sum(diff)/(size(bits_A)+0.0)
    return BMR

def BGR(bits,sampling_time,sampling_period):
    ''' 求比特生成速率 '''
    BGR = size(bits)/(sampling_time*1000.0/sampling_period)
    return BGR

def entropy(p):
    ''' 求信息熵 '''
    if p==0 or p==1:
        return 0
    else:
        return -p*log(p,2)-(1-p)*log(1-p,2)
        
def SecCap(BER_B,BER_E):
    ''' 求安全容量 '''
    return entropy(BER_E) - entropy(BER_B)