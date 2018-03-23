# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

SNR = range(0,31,5)
ptype = ['Random', 'Even']

bob_MSE = array([[-13.7467857,  -8.92763373],
       [-17.48676158, -10.86919189],
       [-21.97246281, -12.61358271],
       [-27.64967497, -14.9618872],
       [-32.73598317, -17.86330612],
       [-38.43057278, -18.69453062],
       [-42.65321231, -18.88381722]])

bob_BER = array([[ 0.10734769,  0.19254717],
       [ 0.05466912,  0.1684696 ],
       [ 0.0216229,   0.15188155],
       [ 0.00681723,  0.14548742],
       [ 0.0021166,   0.12676101],
       [ 0.00064076,  0.14462264],
       [ 0.00015231,  0.1440566]])

SC = array([[ 0.52319569,  0.03976407],
       [ 0.70209723, -0.04830166],
       [ 0.8530099 ,  0.02344127],
       [ 0.94307637, -0.00486084],
       [ 0.97851096, -0.0116633 ],
       [ 0.99227858,  0.00560601],
       [ 0.99737562, -0.03364716]])

plt.figure(figsize=(8,5))
plt.plot(SNR,bob_MSE[:,0],'ko-',label=ptype[0])
plt.plot(SNR,bob_MSE[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,bob_BER[:,0],'ko-',label=ptype[0])
plt.semilogy(SNR,bob_BER[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(SNR,SC[:,0],'ko-',label=ptype[0])
plt.plot(SNR,SC[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()
plt.show()