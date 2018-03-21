# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

order = [1,2,3,4,5]
qtype = ['natural','gray']

bob_MSE = array([[-32.32539365, -32.31408161],
       [-30.67636158, -31.34270116],
       [-26.0755642 , -30.61408353],
       [-15.96402329, -30.37826364],
       [ -6.52353313, -18.83375209]])
eva_MSE = array([[ 2.97688258,  2.96454932],
       [ 3.22109222,  3.11757834],
       [ 3.07603134,  2.91174602],
       [ 3.14120706,  3.07478146],
       [ 2.97715363,  2.96196227]])

bob_BER = array([[ 0.00954307,  0.00415966],
       [ 0.01203782,  0.00902311],
       [ 0.06879202,  0.01592962],
       [ 0.18157563,  0.03064076],
       [ 0.32569853,  0.14707983]])

eva_BER = array([[ 0.49259454,  0.48939076],
       [ 0.4946271 ,  0.49094538],
       [ 0.49173319,  0.49253676],
       [ 0.49305147,  0.49243697],
       [ 0.49103992,  0.49154412]])

SC = array([[ 0.95027287,  0.95027287],
       [ 0.94565398,  0.95389902],
       [ 0.7580192 ,  0.92612239],
       [ 0.44092909,  0.88225352],
       [ 0.14135312,  0.53179117]])

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