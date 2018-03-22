# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

m = range(2,9)

bob_MSE = array([-33.17913401, -31.98874969, -27.42364325, -11.63853619,
        -3.94066881,  -1.68036263,  -2.35859229])

eva_MSE = array([ 3.06304387,  2.96786964,  3.13552755,  3.02056622,  3.0562999 ,
        3.01299805,  3.04262566])

bob_BER = array([ 0.00189601,  0.00902311,  0.0504937 ,  0.22845063,  0.37273109,
        0.40893382,  0.40527311])

eva_BER = array([ 0.49295168,  0.49205357,  0.49255777,  0.49363445,  0.49389706,
        0.49184874,  0.49244748])

SC = array([ 0.98021335,  0.95148486,  0.81918748,  0.32038139,  0.08293778,
        0.03341059,  0.03758616])

plt.figure(figsize=(8,5))
plt.plot(m,bob_MSE,'ko-')
plt.xlabel('m')
plt.ylabel('MSE(dB)')
plt.title('MSE')

plt.figure(figsize=(8,5))
plt.semilogy(m,bob_BER,'ko-')
plt.xlabel('m')
plt.ylabel('BER')
plt.title('BER')

plt.figure(figsize=(8,5))
plt.plot(m,SC,'ko-')
plt.xlabel('m')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')