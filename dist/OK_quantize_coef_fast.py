# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

coef = [i/10.0 for i in range(10)]

bob_MSE = array([ -2.45290821,  -5.85291662,  -9.88914197, -16.287057  ,
       -21.54394295, -26.53668777, -28.76593104, -30.82421968,
       -31.62807819, -32.60874924])

eva_MSE = array([ 2.93583439,  3.05925014,  3.10111479,  3.00732457,  3.04731222,
        2.97133053,  2.94995532,  2.98458993,  3.03755737,  3.08137099])

bob_BER = array([ 0.41597164,  0.34577206,  0.26304622,  0.17382353,  0.11      ,
        0.05795693,  0.03182248,  0.02415966,  0.01377101,  0.00474265])

eva_BER = array([ 0.49184349,  0.49372899,  0.49047269,  0.49397584,  0.49328782,
        0.49162815,  0.49192752,  0.49403361,  0.49440651,  0.49454832])

SC = array([ 0.02994025,  0.10189222,  0.23826628,  0.45980933,  0.62558674,
        0.78838822,  0.86946024,  0.90811329,  0.94055577,  0.96716032])

plt.figure(figsize=(8,5))
plt.plot(coef,bob_MSE,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('MSE(dB)')
plt.title('MSE')

plt.figure(figsize=(8,5))
plt.semilogy(coef,bob_BER,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('BER')
plt.title('BER')

plt.figure(figsize=(8,5))
plt.plot(coef,SC,'ko-')
plt.xlabel('Coefficient')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')