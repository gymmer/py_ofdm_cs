# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4]

lx_MSE = array([-32.67437859, -33.06206353, -33.08406421, -33.39558238])

CS_MSE = array([-31.79705005, -31.38202346, -31.48027674, -28.13684376])

eva_MSE = array([ 3.06523469,  2.93694023,  3.01912074,  3.11370457])

lx_BER = array([ 0.00216387,  0.0021166 ,  0.00218487,  0.00207458])

CS_BER = array([ 0.01068277,  0.0106145 ,  0.01488971,  0.04976366])

eva_BER = array([ 0.49344538,  0.48965861,  0.49493172,  0.49332458])

lx_SC = array([ 0.97803242,  0.97870087,  0.9780754 ,  0.97886571])

CS_SC = array([ 0.95246035,  0.94346172,  0.93182147,  0.81826121])

plt.figure(figsize=(8,5))
plt.plot(order,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(order,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(order,eva_MSE,'ks--',label='Eve')
plt.xlabel('Quantize Order')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(order,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(order,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(order,eva_BER,'ks--',label='Eve')
plt.xlabel('Quantize Order')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(order,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(order,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Quantize Order')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()
