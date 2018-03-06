# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import array

w = [i/10.0 for i in range(11)]
bmr = array([ 0.0146344 ,  0.01684184,  0.01752003,  0.02016126,  0.02174755,
        0.02285133,  0.02487454,  0.02751753,  0.02879507,  0.03110392,
        0.03246641])

plt.figure(figsize=(8,5))
plt.plot(w,bmr,'ko-')
plt.xlabel('w')
plt.ylabel('BMR')
plt.title('BMR of different w')
plt.show()