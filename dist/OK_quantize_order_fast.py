# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4]
qtype = ['natural','gray']

bob_MSE = array([[-32.32539365, -32.31408161],
       [-30.67636158, -31.34270116],
       [-26.0755642 , -30.61408353],
       [-15.96402329, -30.37826364]])
eva_MSE = array([[ 2.97688258,  2.96454932],
       [ 3.22109222,  3.11757834],
       [ 3.07603134,  2.91174602],
       [ 3.14120706,  3.07478146]])

bob_BER = array([[ 0.00731618,  0.00902836],
       [ 0.01542542,  0.01883929],
       [ 0.06418067,  0.0157563 ],
       [ 0.17707458,  0.02993697]])

eva_BER = array([[ 0.49259454,  0.48939076],
       [ 0.4946271 ,  0.49094538],
       [ 0.49173319,  0.49253676],
       [ 0.49305147,  0.49243697]])

SC = array([[ 0.95888444,  0.95519888],
       [ 0.92191716,  0.92630508],
       [ 0.77837773,  0.93135054],
       [ 0.45145482,  0.8845795 ]])

plt.figure(figsize=(8,5))
plt.plot(order,bob_MSE[:,0],'ko-',label=qtype[0])
plt.plot(order,bob_MSE[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(order,bob_BER[:,0],'ko-',label=qtype[0])
plt.semilogy(order,bob_BER[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(order,SC[:,0],'ko-',label=qtype[0])
plt.plot(order,SC[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()