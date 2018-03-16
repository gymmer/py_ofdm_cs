# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

iteration = [0,1,2,3,4]

lx_MSE = array([-32.92183828, -32.92818289, -32.76025946, -33.19932997, -33.58817415])

CS_MSE = array([ -4.52097299, -19.38605112, -31.10382403, -33.19932997, -33.58817415])

eva_MSE = array([ 2.93431392,  3.00369884,  3.10683742,  3.09302825,  3.04603779])

lx_BER = array([ 0.00216387,  0.00215336,  0.00207983,  0.00204832,  0.00189076])

CS_BER = array([ 0.35533088,  0.12404937,  0.01360294,  0.00204832,  0.00189076])

eva_BER = array([ 0.49021008,  0.49342437,  0.49198529,  0.49427521,  0.49532563])

lx_SC = array([ 0.97840165,  0.97839445,  0.97862289,  0.97895919,  0.98080651])

CS_SC = array([ 0.08443588,  0.58789389,  0.9426155 ,  0.97895919,  0.98080651])

plt.figure(figsize=(8,5))
plt.plot(iteration,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(iteration,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(iteration,eva_MSE,'ks--',label='Eve')
plt.xlabel('Iteration')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(iteration,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(iteration,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(iteration,eva_BER,'ks--',label='Eve')
plt.xlabel('Iteration')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(iteration,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Iteration')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()