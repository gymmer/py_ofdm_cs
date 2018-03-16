# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

coef = [i/10.0 for i in range(10)]

lx_MSE = array([-33.04221337, -32.71387787, -32.55084464, -32.71726914,
       -32.81551822, -33.06436054, -33.06420123, -33.0434016 ,
       -32.70335673, -32.98308574])

CS_MSE = array([ -2.45290821,  -5.85291662,  -9.88914197, -16.287057  ,
       -21.54394295, -26.53668777, -28.76593104, -30.82421968,
       -31.62807819, -32.60874924])

eva_MSE = array([ 2.93583439,  3.05925014,  3.10111479,  3.00732457,  3.04731222,
        2.97133053,  2.94995532,  2.98458993,  3.03755737,  3.08137099])

lx_BER = array([ 0.00204832,  0.00206408,  0.00205882,  0.00233193,  0.00228992,
        0.00192752,  0.00196429,  0.00205882,  0.00230042,  0.00219538])

CS_BER = array([ 0.41597164,  0.34577206,  0.26304622,  0.17382353,  0.11      ,
        0.05795693,  0.03182248,  0.02415966,  0.01377101,  0.00474265])

eva_BER = array([ 0.49184349,  0.49372899,  0.49047269,  0.49397584,  0.49328782,
        0.49162815,  0.49192752,  0.49403361,  0.49440651,  0.49454832])

lx_SC = array([ 0.9792666 ,  0.97890504,  0.97865989,  0.97672366,  0.97735015,
        0.98025622,  0.97974738,  0.97965162,  0.97694234,  0.97787027])

CS_SC = array([ 0.02994025,  0.10189222,  0.23826628,  0.45980933,  0.62558674,
        0.78838822,  0.86946024,  0.90811329,  0.94055577,  0.96716032])

plt.figure(figsize=(8,5))
plt.plot(coef,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(coef,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(coef,eva_MSE,'ks--',label='Eve')
plt.xlabel('Coefficient')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(coef,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(coef,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(coef,eva_BER,'ks--',label='Eve')
plt.xlabel('Coefficient')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(coef,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(coef,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Coefficient')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()