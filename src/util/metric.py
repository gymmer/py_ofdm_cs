# -*- coding: utf-8 -*-

from numpy import mean,size,abs,sum,floor,zeros,random
from math import log,log10,sqrt,erfc

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
    
def UST(bits):
    '''
    universal_statistical_test  通用统计测试
    
    密钥随机性测试
    
    一种统计检测项目，用于检测待检序列能否被压缩（无损压缩）。
    如果待检序列能被显著地压缩，那么就认为该序列不是随机的。
    假设通用统计测试值为P-value，显著性水平a=0.01，
    则如果 P-value > a ，通过检测，序列是随机的
    如果 P-value < a ，则未通过检测，序列不是随机的
    '''
    n = size(bits)
    expected = [0, 0, 0, 0, 0, 0, 5.2177052, 6.1962507, 7.1836656,8.1764248, 
                9.1723243, 10.170032, 11.168765,12.168070, 13.167693, 14.167488, 15.167379]
    variance = [0, 0, 0, 0, 0, 0, 2.954, 3.125, 3.238, 3.311, 3.356, 
                3.384,3.401, 3.410, 3.416, 3.419, 3.421]
    
    L = 6.0
    if n >= 387840:     L = 6.0
    if n >= 904960:     L = 7.0
    if n >= 2068480:    L = 8.0
    if n >= 4654080:    L = 9.0
    if n >= 10342400:   L = 10.0
    if n >= 22753280:   L = 11.0
    if n >= 49643520:   L = 12.0
    if n >= 107560960:  L = 13.0
    if n >= 231669760:  L = 14.0
    if n >= 496435200:  L = 15.0
    if n >= 1059061760: L = 16.0
        
    Q = 10.0*2.0**L
    K = floor(n/L)-Q
    
    p = 2.0**L
    c = 0.7-0.8/L+(4.0+32.0/L)*(K**(-3.0/L))/15.0
    sigma = c*sqrt(variance[int(L)]/K)
    T = zeros(p)
    
    for i in range(1,int(Q+1)):
        decRep = 0.0
        for j in range(int(L)):
            decRep += bits[int((i-1)*L+j)]*2**(L-1-j)
        T[decRep] = i
    
    total = 0.0
    for i in range(int(Q+1),int(Q+K+1)):
        decRep = 0.0
        for j in range(int(L)):
            decRep += bits[int((i-1)*L+j)]*2**(L-1-j)
        total += log(i-T[decRep],2)
        T[decRep] = i
        
    phi = total/K
    arg = (phi-expected[int(L)])/sigma
    p_value = erfc(abs(arg)/sqrt(2))
    return p_value

if __name__ == "__main__":   
    bits = random.randint(0,2,4000)
    print '%.2f' % (UST(bits))