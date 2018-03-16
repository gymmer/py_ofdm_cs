# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = range(5,41,5)

lx_MSE = array([-32.92231409, -32.81815198, -32.81333796, -32.70121976,
       -32.97503557, -32.89319018, -32.72093642, -32.67555966])

CS_MSE = array([-13.95416075, -26.64481231, -30.20509698, -31.7560881 ,
       -32.38215805, -32.09201141, -32.17471339, -32.67555966])

eva_MSE = array([ 3.0108745 ,  3.02966631,  3.08381762,  2.9549035 ,  3.13355116,
        3.04445533,  3.15563769,  3.07799424])

lx_BER = array([ 0.00233718,  0.00216912,  0.00209559,  0.00185924,  0.0017437 ,
        0.00219013,  0.00219538,  0.0023792 ])

CS_BER = array([ 0.20899685,  0.04618697,  0.02782038,  0.01283088,  0.00815126,
        0.00868172,  0.00584034,  0.0023792 ])

eva_BER = array([ 0.4935084 ,  0.49285189,  0.49179097,  0.4921271 ,  0.49173845,
        0.49069328,  0.49211134,  0.49351366])

lx_SC = array([ 0.97661374,  0.97793541,  0.9791564 ,  0.98090312,  0.98180129,
        0.97793663,  0.97769754,  0.97644737])

CS_SC = array([ 0.36555092,  0.82262024,  0.89324367,  0.94195134,  0.96174766,
        0.95513224,  0.96437453,  0.97644737])

plt.figure(figsize=(8,5))
plt.plot(block_size,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(block_size,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(block_size,eva_MSE,'ks--',label='Eve')
plt.xlabel('Block size')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(block_size,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(block_size,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(block_size,eva_BER,'ks--',label='Eve')
plt.xlabel('Block size')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(block_size,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(block_size,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Block size')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()