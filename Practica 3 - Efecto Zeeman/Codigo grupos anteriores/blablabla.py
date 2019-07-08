# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:16:49 2019

@author: Publico
"""

import matplotlib.pyplot as plt
import numpy as np

ch2_mean, ch2_std = np.load('volt_ch2.npy')
tempRead = np.load('tempRead.npy')
timeTemp = np.load('timeTemp.npy')
tempSet = np.load('tempSet.npy')

plt.figure(3)
plt.plot(tempRead, ch2_mean, '.')
plt.pause(0.01)
plt.show()
    
plt.figure(4)
plt.plot(ch2_mean)
plt.pause(0.01)
plt.show()
    
plt.figure(5)
plt.plot(tempRead,'.')
plt.pause(0.01)
plt.show()
    
plt.figure(6)
plt.plot(tempSet,'.')
plt.pause(0.01)
plt.show()