# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:11:23 2019

@author: Publico
"""
#import visa
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from instrumentos import Osciloscopio

osci = Osciloscopio('USB0::0x0699::0x0363::C102220::INSTR')
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

#%% Medicion de la deriva.
i = 0
while i < 45:
    time.sleep(60)
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    medicion = [tiempo1,data1,data2]
    #Medicion tiene 3 columnas, la 1 los tiempos, la 2 el voltaje Channel 1, 
    #la 3 el voltaje channel 2.
    print ("Medición"+str(i)+"terminada")
    np.asarray(medicion)
    np.save("Medicion_"+str(i),medicion)
    i = i + 1
    
#%% Barrido de la DAVS en temperatura
T0 = 22.45
T = 22.45
i=1
while T < 22.56:
    temp_set(tec, T0 + 0.005*i)
    time.sleep(17)
    temp = np.array(temp_read(tec))
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    medicion = [data1,data2,temp]
    #Medicion tiene 3 columnas, la 1 el voltaje del canal 1 , la 2 el voltaje del canal 2, 
    #la 3 la temperatura a la cual se obtienen esos voltajes.
    print ("Medición"+str(i)+"terminada")
    np.asarray(medicion)
    temp = np.around (temp,2)
    np.save("Medicion_"+str(i)+"_BarridoTemp"+str(temp),medicion) 
    
    T = temp_read(tec)
    i = i + 1
#%%
temp_set (tec, 22.45)