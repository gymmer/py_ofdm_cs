# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import arange,array

SNR = range(0,31,5)
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # CS估计导频数，P<N
pos_even = arange(1,N,15)   # 均匀导频图样

random_MSE = array([
    -13.7467857 , -17.48676158, -21.97246281, -27.64967497,
    -32.73598317, -38.43057278, -42.65321231
])

even_MSE = array([
    -8.92763373, -10.86919189, -12.61358271, -14.9618872 ,
    -17.86330612, -18.69453062, -18.88381722
])

random_BER = array([
    0.10734769,  0.05466912,  0.0216229 ,  0.00681723,  0.0021166 ,
    0.00064076,  0.00015231
])

even_BER = array([
    0.19254717,  0.1684696 ,  0.15188155,  0.14548742,  0.12676101,
    0.14462264,  0.1440566
])

random_SC = array([
    0.52319569,  0.70209723,  0.8530099 ,  0.94307637,  0.97851096,
    0.99227858,  0.99737562
])

even_SC = array([
    0.03976407, -0.04830166,  0.02344127, -0.00486084, -0.0116633 ,
    0.00560601, -0.03364716
])

plt.figure(figsize=(8,5))
plt.plot(SNR,random_MSE,'ko-',label='Random')
plt.plot(SNR,even_MSE,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,random_BER,'ko-',label='Random')
plt.semilogy(SNR,even_BER,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(SNR,random_SC,'ko-',label='Random')
plt.plot(SNR,even_SC,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()
plt.show()