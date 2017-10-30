# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

block_size = range(5,41,5)
coef = 0.8
iteration = [0,1,2,3,4]

bmr = array([
    [1.298530570715934196e-01,8.519844922138945786e-02,4.288563367094314766e-02,1.411479513206052860e-02,1.741932873623044638e-03],
    [5.842082400940496606e-02,2.187305009237017553e-02,3.965297155287803889e-03,2.012704625229087016e-04,0.000000000000000000e+00],
    [4.287437033181991375e-02,1.259924598088177534e-02,1.002806130506030428e-03,4.081632653061225183e-05,0.000000000000000000e+00],
    [3.510894741546825848e-02,7.916806862369845862e-03,9.853064902570225075e-04,0.000000000000000000e+00,0.000000000000000000e+00],
    [3.118580286505513721e-02,7.293866908421978677e-03,3.965194536003056620e-04,3.759398496240601322e-05,0.000000000000000000e+00],
    [2.510956062173655412e-02,4.596492320685241148e-03,1.203481392557022864e-04,	0.000000000000000000e+00,0.000000000000000000e+00],
    [2.431819563850338983e-02,3.370817159081794957e-03,4.800846993538023335e-05,1.956947162426614535e-05,0.000000000000000000e+00],
    [1.835913603144318992e-02,2.440049316441139041e-03,1.028604212769445095e-04,0.000000000000000000e+00,0.000000000000000000e+00]
])

bgr = array([
    [3.205100000000000726e-01,2.808633333333332427e-01,2.433433333333334114e-01,2.122166666666667478e-01,1.846600000000000186e-01],
    [2.509799999999999809e-01,2.187500000000001388e-01,1.910766666666666724e-01,1.652933333333334032e-01,1.439199999999999646e-01],
    [2.453566666666666396e-01,2.134766666666667312e-01,1.851266666666666061e-01,1.616766666666667185e-01,1.401166666666665839e-01],
    [2.460033333333332684e-01,2.125200000000001255e-01,1.853833333333332611e-01,1.611633333333332974e-01,1.401399999999999868e-01],
    [2.655233333333332779e-01,2.323300000000000642e-01,2.012500000000000955e-01,1.761899999999999300e-01,1.523433333333333306e-01],
    [2.560399999999999898e-01,2.231366666666668441e-01,1.948100000000000387e-01,1.688166666666667259e-01,1.465100000000000013e-01],
    [2.620100000000000207e-01,2.289233333333333398e-01,1.974933333333334096e-01,1.726200000000000789e-01,1.496600000000000152e-01],
    [2.594599999999998574e-01,2.260533333333333283e-01,1.962100000000000510e-01,1.709633333333333838e-01,1.475833333333333719e-01]
])

''' block_size为横坐标'''
plt.figure(figsize=(8,5))
plt.plot(block_size,bmr[:,0],'ro-',label='No winnow')
plt.plot(block_size,bmr[:,1],'yo-',label='1 interation')
plt.plot(block_size,bmr[:,2],'go-',label='2 interations')
plt.plot(block_size,bmr[:,3],'bo-',label='3 interations')
plt.plot(block_size,bmr[:,4],'ko-',label='4 interations')
plt.xlabel('Block size')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different block sizes(coef=%.2f)'%coef)
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(block_size,bgr[:,0],'ro-',label='No winnow')
plt.plot(block_size,bgr[:,1],'yo-',label='1 interation')
plt.plot(block_size,bgr[:,2],'go-',label='2 interations')
plt.plot(block_size,bgr[:,3],'bo-',label='3 interations')
plt.plot(block_size,bgr[:,4],'ko-',label='4 interations')
plt.xlabel('Block size')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different block sizes(coef=%.2f)'%coef)
plt.legend()
plt.ylim(0,1)

'''iteration为横坐标'''
plt.figure(figsize=(8,5))
plt.plot(iteration,bmr[0,:],'ro-',label='bl=%d'%(block_size[0]))
plt.plot(iteration,bmr[2,:],'yo-',label='bl=%d'%(block_size[2]))
plt.plot(iteration,bmr[4,:],'go-',label='bl=%d'%(block_size[4]))
plt.plot(iteration,bmr[6,:],'bo-',label='bl=%d'%(block_size[6]))
plt.xlabel('Iteration')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different iteration(coef=%.2f)'%(coef))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr[0,:],'ro-',label='bl=%d'%(block_size[0]))
plt.plot(iteration,bgr[2,:],'yo-',label='bl=%d'%(block_size[2]))
plt.plot(iteration,bgr[4,:],'go-',label='bl=%d'%(block_size[4]))
plt.plot(iteration,bgr[6,:],'bo-',label='bl=%d'%(block_size[6]))
plt.xlabel('Iteration')
plt.ylabel('Bit Generation Rate')
plt.title('BGR of different iteration(coef=%.2f)'%(coef))
plt.legend()
