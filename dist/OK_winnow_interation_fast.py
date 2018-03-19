# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

iteration = [0,1,2,3,4]

bob_MSE = array([ -4.52097299, -19.38605112, -31.10382403, -33.19932997, -33.58817415])

eva_MSE = array([ 2.93431392,  3.00369884,  3.10683742,  3.09302825,  3.04603779])

bob_BER = array([ 0.35533088,  0.12404937,  0.01360294,  0.00204832,  0.00189076])

eva_BER = array([ 0.49021008,  0.49342437,  0.49198529,  0.49427521,  0.49532563])

SC = array([ 0.08443588,  0.58789389,  0.9426155 ,  0.97895919,  0.98080651])

plt.figure(figsize=(8,5))
plt.plot(iteration,bob_MSE,'ko-')
plt.xlabel('Iteration')
plt.ylabel('MSE(dB)')
plt.title('MSE')

plt.figure(figsize=(8,5))
plt.semilogy(iteration,bob_BER,'ko-')
plt.xlabel('Iteration')
plt.ylabel('BER')
plt.title('BER')

plt.figure(figsize=(8,5))
plt.plot(iteration,SC,'ko-')
plt.xlabel('Iteration')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')