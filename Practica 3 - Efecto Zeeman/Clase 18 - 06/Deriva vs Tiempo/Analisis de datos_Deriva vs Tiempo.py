# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 23:01:45 2019

@author: juan
"""

import numpy as np
import os
import matplotlib.pyplot as plt 
#%%
total_mediciones = []
files_list = os.listdir('.')
tiempo, davs = [], []
files_list.pop(0)

for s in files_list:
    data = np.load(s)
    tiempo.append(data[0])
    davs.append(data[2])
print(len(davs[0]))
#%%
#print(tiempo,davs)
    
plt.title ("Medicion de la señal del laser" "\n" "durante 45 minutos")
plt.xlabel("Tiempo(s)")
plt.ylabel("Voltaje(V)")
plt.grid()
plt.xlim(-0.006,-0.002)
plt.ylim(-0.05,0.11)
plt.plot(tiempo[0],davs[0],'-', color ="b")
plt.plot(tiempo[20],davs[20],'-', color ="g")
plt.plot(tiempo[30],davs[30],'-', color ="r")
plt.plot(tiempo[44],davs[44],'-', color ="m")
plt.legend(("1 Minuto","20 Minutos","30 Minutos","45 Minutos"))