# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:18:14 2019

@author: Publico
"""

#%%
import numpy as np
import matplotlib.pyplot as plt

from instrumentos import Osciloscopio
osci = Osciloscopio('USB::0x0699::0x0363::C102220::INSTR')
#%% Inicio y configuracion del ITC4001
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
#%% Barrido de la DAVS en temperatura
tempArray=[]
T0=22.44
T = 22.45
i=1
while T < 22.56:
    temp_set(tec, T0 + 0.001*i)
    plt.pause(1)
    temp = np.array(temp_read(tec))
    #tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    measurement_name = str(i)
    #ch1 = np.array([tiempo1, data1])
    ch2 = np.array([tiempo2, data2])
    np.save('temp'+measurement_name, temp)
    #np.save('volt_ch1_'+measurement_name, ch1)
    np.save('volt_ch2_'+measurement_name, ch2)
    T = temp_read(tec)
    i = i + 1
#%% Funcionando 'P' PRIMERO Y SEGUNDO INTENTO
import time

v0 = 0 #A determinar de estudiar la DAVS barrida en T
deltaT = 0.001 #A pensar 
t = 0
i=0
while True:
    t0 = time.time()
    while t - t0 < 5:
        T = temp_read(tec)
        tempRead = np.array(T)
        tiempo1, data1 = osci.get_ventana(1)
        tiempo2, data2 = osci.get_ventana(2)
        ch1 = np.array([tiempo1, data1])
        ch2 = np.array([tiempo2, data2])
        measurement_name = str(i)
        np.save('tempRead'+measurement_name, tempRead)
        np.save('volt_ch1_'+measurement_name, ch1)
        np.save('volt_ch2_'+measurement_name, ch2)
        i = i + 1
        t = time.time()
    
    v = np.mean(data2)
    #El P no deberia ejecutarse en cada instancia de levantar datos. Hay que considerar un tiempo de acomodamiento del sistema una vez que se le modifica la temperatura. Pensamos que si e tiempo de acomodamiento es del orden de un numero "entero" de veces el tiempo en el que medimos podemos hacer un contador aparte de ese numero de veces.
    if v > v0:
        temp_set(tec, T - deltaT)
        tempSet = np.array(T-deltaT)
    elif v < v0:
        temp_set(tec, T + deltaT)
        tempSet = np.array(T+deltaT)
    np.save('tempSet'+measurement_name, tempSet)
    #plt.pause(60) #A pensar
#%%
v0 = 0 #A determinar de estudiar la DAVS barrida en T
deltaT = 0.001 #A pensar 
t = 0
volt_ch1 = []
volt_ch2 = []
T=22.497
ch1_mean, ch1_std = [], []
ch2_mean, ch2_std = [], []
timeTemp = []
tempRead = []
tempSet = []
t0 = time.time()
plt.ion()
while True:
    tempRead = np.append(tempRead, temp_read(tec))
    timeTemp = np.append(timeTemp, time.time()-t0)
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    volt1 = np.mean(data1) #Señal directa
    volt2 = np.mean(data2) #DAVS
    volt1Std = np.std(data1)
    volt2Std = np.std(data2)
    #El P no deberia ejecutarse en cada instancia de levantar datos. Hay que considerar un tiempo de acomodamiento del sistema una vez que se le modifica la temperatura. Pensamos que si e tiempo de acomodamiento es del orden de un numero "entero" de veces el tiempo en el que medimos podemos hacer un contador aparte de ese numero de veces.
    error = v0 - volt2
    if np.abs(error) >= 0.2:
        if error < 0:
            T = T+deltaT
            temp_set(tec, T)
        elif error > 0:
            T = T - deltaT
            temp_set(tec, T)
            
    tempSet = np.append(tempSet, T)
    ch1_mean=np.append(ch1_mean, volt1)
    ch1_std=np.append(ch1_std, volt1Std)
    ch2_mean=np.append(ch2_mean, volt2)
    ch2_std=np.append(ch2_std, volt2Std)
    
    plt.figure(3)
    plt.plot(tempRead, ch2_mean, '.')
    plt.pause(0.01)
    plt.show()
    
    plt.figure(4)
    plt.plot(timeTemp, ch2_mean)
    plt.pause(0.01)
    plt.show()
    
    plt.figure(5)
    plt.plot(timeTemp, tempRead,'.')
    plt.pause(0.01)
    plt.show()
    
    plt.figure(6)
    plt.plot(timeTemp, tempSet,'.')
    plt.pause(0.01)
    plt.show()
    
    print(T)
    #plt.pause(60) #A pensar
#%%
data_ch1 = np.vstack((np.array(ch1_mean), np.array(ch1_std)))
data_ch2 = np.vstack((np.array(ch2_mean), np.array(ch2_std)))
    
np.save('volt_ch1', data_ch1)
np.save('volt_ch2', data_ch2)
np.save('tempRead', tempRead)
np.save('tempSet', tempSet)
np.save('time', timeTemp)