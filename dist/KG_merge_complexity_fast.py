# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

sampling_time = range(1,20,1)
times = array([[   39. ,     7.5,    55. ,    47. ,    50.5,    46.5,    47.5],
       [   76.5,    27.5,   116. ,   103.5,   104. ,   104. ,   105. ],
       [  163.5,    42. ,   193.5,   171.5,   171. ,   170. ,   210.5],
       [  185. ,    63.5,   270.5,   246. ,   265. ,   234.5,   242. ],
       [  258. ,    70. ,   367.5,   320. ,   328. ,   336. ,   320.5],
       [  343.5,    78.5,   476.5,   421.5,   430. ,   414. ,   445.5],
       [  422. ,    93.5,   570.5,   523.5,   531. ,   523.5,   531.5],
       [  523.5,   109.5,   706. ,   648.5,   633. ,   648. ,   675. ],
       [  642.5,   132.5,   895. ,   844.5,   777. ,   806. ,   792.5],
       [  785. ,   145.5,  1023. ,   993.5,   922. ,   923.5,   932. ],
       [  929.5,   156. ,  1148.5,  1078. ,  1096.5,  1086. ,  1078. ],
       [ 1054.5,   172. ,  1289. ,  1218.5,  1238. ,  1265.5,  1250. ],
       [ 1311. ,   204. ,  1502.5,  1378. ,  1406.5,  1383. ,  1399. ],
       [ 1382.5,   211. ,  1672. ,  1570.5,  1578. ,  1578. ,  1609.5],
       [ 1547. ,   250. ,  1843.5,  1781.5,  1811.5,  1789. ,  1750. ],
       [ 1750. ,   242.5,  2063.5,  1969. ,  1953. ,  1984.5,  1976.5],
       [ 1901.5,   266. ,  2312.5,  2184. ,  2156.5,  2172. ,  2179.5],
       [ 2101.5,   281. ,  2523.5,  2372. ,  2417.5,  2439.5,  2503. ],
       [ 2400.5,   293. ,  2874.5,  2760.5,  2629. ,  2669. ,  2631.5]])
       
plt.figure(figsize=(8,5))
plt.plot(sampling_time,times[:,0],'ko-', label='RSSI Only')
plt.plot(sampling_time,times[:,1],'k^:', label='Phase Only')
plt.plot(sampling_time,times[:,2],'ks--',label='Cross')
plt.plot(sampling_time,times[:,3],'ro-',label='AND')
plt.plot(sampling_time,times[:,4],'go-',label='OR')
plt.plot(sampling_time,times[:,5],'bo-',label='Xor')
plt.plot(sampling_time,times[:,6],'yo-',label='Syn')
plt.xlabel('Sampling Time(s)')
plt.ylabel('Time(ms)')
plt.title('Time of different sampling time')
plt.legend()
plt.show()