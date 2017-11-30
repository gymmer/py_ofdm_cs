# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import arange,array

SNR = range(0,31,5)
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # CS估计导频数，P<N
pos_ls = arange(0,N,5)      # LS估计的均匀导频图样

CS_MSE = array([-12.91947905, -18.41703987, -23.00347076, -28.11697554,
       -33.29921024, -37.75578647, -42.8740129 ])

CS_BER = array([ 0.11544643,  0.04758403,  0.01915966,  0.00629727,  0.00182248,
        0.00061975,  0.00027311])

LS_MSE = array([ -9.86169658, -12.14495089, -13.4433354 , -13.64853738,
       -13.40936531, -14.02741247, -13.89044002])

LS_BER = array([ 0.15578851,  0.10189487,  0.0740709 ,  0.06553178,  0.06363692,
        0.05954768,  0.06026284])

CS_SC = array([ 0.49381484,  0.73277615,  0.8679723 ,  0.94639922,  0.98128938,
        0.99229593,  0.99622225])

LS_SC = array([ 0.00328107, -0.01683116,  0.00695385, -0.00864503, -0.00594933,
        0.02370059, -0.00297679])

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE,'g*-',label='CS(Random, P=%s)'%(P))
plt.plot(SNR,LS_MSE,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER,'g*-',label='CS(Random, P=%s)'%(P))
plt.semilogy(SNR,LS_BER,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_SC,'g*-',label='CS(Random, P=%s)'%(P))
plt.plot(SNR,LS_SC,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity')
plt.title('Security Capacity')
plt.legend()