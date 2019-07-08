# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:08:08 2019

@author: Publico
"""
import numpy as np
import matplotlib.pyplot as plt

ch1 = np.load('canal2_sinB_absorcion_23.5C_13_14.npy')

tiempo1 = ch1[0]
data1 = ch1[1]

plt.figure(1)
plt.title('Voltaje vs Tiempo', size = 16)
plt.plot(tiempo1,data1, label='CH1')
plt.xlabel('Tiempo[ms]', size=12)
plt.ylabel('Voltaje[mV]', size=12)
plt.legend()
plt.show()