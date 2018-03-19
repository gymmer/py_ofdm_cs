# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = range(5,41,5)

bob_MSE = array([-13.95416075, -26.64481231, -30.20509698, -31.7560881 ,
       -32.38215805, -32.09201141, -32.17471339, -32.67555966])

eva_MSE = array([ 3.0108745 ,  3.02966631,  3.08381762,  2.9549035 ,  3.13355116,
        3.04445533,  3.15563769,  3.07799424])

bob_BER = array([ 0.20899685,  0.04618697,  0.02782038,  0.01283088,  0.00815126,
        0.00868172,  0.00584034,  0.0023792 ])

eva_BER = array([ 0.4935084 ,  0.49285189,  0.49179097,  0.4921271 ,  0.49173845,
        0.49069328,  0.49211134,  0.49351366])

SC = array([ 0.36555092,  0.82262024,  0.89324367,  0.94195134,  0.96174766,
        0.95513224,  0.96437453,  0.97644737])

plt.figure(figsize=(8,5))
plt.plot(block_size,bob_MSE,'ko-')
plt.xlabel('Block size')
plt.ylabel('MSE(dB)')
plt.title('MSE')

plt.figure(figsize=(8,5))
plt.semilogy(block_size,bob_BER,'ko-')
plt.xlabel('Block size')
plt.ylabel('BER')
plt.title('BER')

plt.figure(figsize=(8,5))
plt.plot(block_size,SC,'ko-')
plt.xlabel('Block size')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')