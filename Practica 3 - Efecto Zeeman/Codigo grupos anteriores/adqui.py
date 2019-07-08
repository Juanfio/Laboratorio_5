# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:07:52 2019

@author: Publico
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import datetime
#%%
import visa
rm = visa.ResourceManager()
tec = rm.open_resource('USB::0x1313::0x804A::M00404166::INSTR')
tec.write('CONF:TEMP')

def temp_set(tec, temp):
        tec.write('SOUR2:TEMP {}C'.format(temp))
        
def temp_sp_read(tec):
        temp_sp = float(tec.query('SOUR2:TEMP?'))
        print(temp_sp)
        return(temp_sp)
        
def temp_read(tec):
        temp = float(tec.query('read?'))
        print(temp)
        return(temp)
#%%
from instrumentos import Osciloscopio
osci = Osciloscopio('USB::0x0699::0x0363::C102220::INSTR')
#%%
tempArray=[]
T=23
i=1
while T > 21.4:
    temp_set(tec, 21.4)
    tempArray = np.append(tempArray, temp_read(tec))
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    measurement_name = str(i)
    ch1 = np.array([tiempo1, data1])
    ch2 = np.array([tiempo2, data2])
    np.save('temp'+measurement_name, tempArray)
    np.save('volt_ch1_'+measurement_name, ch1)
    np.save('volt_ch2_'+measurement_name, ch2)
    T = temp_read(tec)
    i = i + 1
#%%
tempArray=[]
i = 1
while True:
    tempArray = np.append(tempArray, temp_read(tec))
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    ch1 = np.array([tiempo1, data1])
    ch2 = np.array([tiempo2, data2])
    measurement_name = str(i)
    np.save('temp'+measurement_name, tempArray)
    np.save('volt_ch1_'+measurement_name, ch1)
    np.save('volt_ch2_'+measurement_name, ch2)
    i = i + 1
    plt.pause(60)
    
#%%
import numpy as np
import matplotlib.pyplot as plt
numberOfFiles = 63 #numero de archivos
i = 1
volt = []
temp = []
while i <= numberOfFiles:    
    volt_total = np.load('volt'+str(i)+'.npy')
    volt_total = volt_total[0, :]
    volt = np.append(volt, np.mean(volt_total))
    i = i + 1
    
temp = np.load('temp63.npy')
#%%
plt.plot(temp,volt,'.')
plt.grid()
plt.show()
