# -*- coding: utf-8 -*-

from numpy import size,floor,zeros,random
from math import sqrt,log,erfc

def Entropy(bits):
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
    print Entropy(bits)