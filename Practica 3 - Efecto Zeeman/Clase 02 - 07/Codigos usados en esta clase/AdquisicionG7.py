# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:11:23 2019

@author: Publico
"""

# Este archivo tiene los codigos necesarios para la adquisición de los datos.

# import visa
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from instrumentos import Osciloscopio
from control import ITC4001
import scipy as sp
from scipy import stats


# itc = ITC4001('USB::0x1313::0x804A::M00404166::INSTR')
osci = Osciloscopio('USB0::0x0699::0x0363::C065093::INSTR')
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
    #Medicion tiene 3 columnas, la 1 los tiempos, la 2 los voltajes Channel 1, 
    #la 3 voltajes channel 2.
    print ("Medición"+str(i)+"terminada")
    np.asarray(medicion)
    np.save("Medicion_"+str(i),medicion)
    i = i + 1
    
#%% Barrido de la DAVS en temperatura
T0 = 22.90
T = 22.90
Tf = 23.025
i=1
med_total = []
while T < Tf:
    temp_set(tec, T0 + 0.002*i)
    time.sleep(10)
    temp = np.array(temp_read(tec))
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    
    data1 = np.mean(data1)
    data2 = np.mean(data2)
    
    dataDAVS = data1 - data2
    medicion = [data1,data2,dataDAVS,temp]
    med_total.append(medicion)
    #Medicion tiene 3 columnas, la 1 los tiempos, la 2 los voltajes Channel 1, 
    #la 3 voltajes channel 2, y la cuarta columna tiene el valor de temperatura.
    print("Medición"+str(i)+"terminada")
    #np.asarray(medicion)
    #temp = np.around (temp,2)
    T = temp_read(tec)
    i = i + 1
    
    
np.asarray(med_total)
np.save("14.BarridoTempDAVS_22.90_23.025",med_total)
#%%
Tf = 22.90 # temperatura a la cual quiero ir.
temp_set(tec, Tf)
start = time.time()
T = temp_read(tec)
while T>Tf:
    T = temp_read(tec)
    time.sleep(0.01)
end = time.time()
print(end-start)
#%% Este codigo y el de arriba nos sirvieron para hacer el barrido rapido entre "8.Barr.."
# y el "12.Barr.."
T = 22.60
Tf = 24.50
i=1
med_total = []
temp_set(tec, Tf)
start = time.time()
while T < Tf:
    time.sleep(0.01)
    temp = np.array(temp_read(tec))
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    
    data1 = np.mean(data1)
    data2 = np.mean(data2)
    
    dataDAVS = data1 - data2
    medicion = [data1,data2,dataDAVS,temp]
    med_total.append(medicion)
    #Medicion tiene 3 columnas, la 1 los tiempos, la 2 los voltajes Channel 1, 
    #la 3 voltajes channel 2, y la cuarta columna tiene el valor de temperatura.
    print("Medición"+str(i)+"terminada")
    #np.asarray(medicion)
    #temp = np.around (temp,2)
    T = temp_read(tec)
    i = i + 1
    print(time.time()-start)
    
np.asarray(med_total)
np.save("12.BarridoTempDAVS_22.60_24.50",med_total)
#%%
temp_set (tec,22.49)
#%% Esto es para plotear los datos levantados. 
a = np.load ("14.BarridoTempDAVS_22.90_23.025.npy")
x_DAVS = []
y_DAVS = []

x_ch1 = []
y_ch1 = []

x_ch2 = []
y_ch2 = []
for i in a:
    x_DAVS.append (i[3])
    y_DAVS.append (i[2])
    
    x_ch1.append (i[3])
    y_ch1.append (i[0])
    
    x_ch2.append (i[3])
    y_ch2.append (i[1])
    
    
plt.plot(x_DAVS,y_DAVS, ".")
#plt.plot(x_ch1,y_ch1,".")
#plt.plot(x_ch2,y_ch2,".")
#%% Esto es para el barrido de 21.80 a 22.40
import os 
total_mediciones = []
files_list = os.listdir('.')
T_vec, davs_vec = [], []

for s in files_list:
    data = np.load(s)
    T_vec.append(data[3])
    davs_vec.append(np.mean(data[2]))
  
T_vec = np.array(T_vec)
davs_vec = np.array(davs_vec)
T_vec = T_vec[np.argsort(T_vec)]
davs_vec = davs_vec[np.argsort(T_vec)]

fig, ax = plt.subplots(figsize=(8, 8))

ax.set_title ("Barrido de T - Medición DAVS")
ax.set_xlabel ("Temperatura (ºC)")
ax.set_ylabel ("Voltaje (V)")
plt.grid()
fig.savefig('Barrido_de_T_Medicion_DAVS.png', bbox_inches="tight")
plt.plot(T_vec, davs_vec, '-')

    
    
