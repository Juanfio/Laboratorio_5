# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:52:38 2019

@author: juan
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import stats
#%% Esto es solamente para ver como se ven el set de datos graficado.
barrido_3 = np.load ("3.BarridoTempDAVS_21.95_22.50.npy")
barrido_4 = np.load ("4.BarridoTempDAVS_22.20_22.35.npy")

x_3_temp = []
y_3_DAVS = []

x_4_temp = []
y_4_DAVS = []

for i in range (len(barrido_3)):
    x_3_temp.append(barrido_3[i][3])
    y_3_DAVS.append(barrido_3[i][2])
    
for i in range (len(barrido_4)):
    x_4_temp.append(barrido_4[i][3])
    y_4_DAVS.append(barrido_4[i][2])

plt.title ("Señal DAVS - Voltaje vs Temperatura")
plt.xlabel ("Temperatura (°C)")
plt.ylabel ("Voltaje (V)")
plt.grid ()
plt.plot (x_3_temp,y_3_DAVS,".")
plt.plot (x_4_temp,y_4_DAVS,".")
#print (barrido_3[0][3])
#%%
# Para el analisis tomo solo el barrido 4. Este tiene mayor cantidad de puntos entre las temperaturas
# de interes. Solo tomo la parte lineal de estos datos, los cuales estan en el rango [65,110].
barrido_4 = np.load ("4.BarridoTempDAVS_22.20_22.35.npy")

x_4_temp = []
y_4_DAVS = []

for i in range (len(barrido_4)):
    x_4_temp.append(np.round(barrido_4[i][3],5))
    y_4_DAVS.append(barrido_4[i][2])

# Pendiente de la recta, ordenada al origen y matriz de covarianza.
# La pendiente depende del rango de valores en los cuales realizo el ajuste lineal.
# Por ejemplo: x_4_temp[93:100] en este rango de temperaturas es bastante pronunciada la pendiente.
POC = np.polyfit (x_4_temp[65:110],y_4_DAVS[65:110],1,cov=True) 
# Varianza de los parametros.
var_pendiente = POC[1][0][0]
var_ordenada = POC[1][1][1]

a = POC[0][0]
b = POC[0][1]
f_lineal = lambda x: a*x+b

# Para el ploteo de la lineal.
rango = np.linspace (min (x_4_temp[65:110]),max (x_4_temp[65:110]),1000)

# Para hallar la temperatura donde es cero el voltaje, utilizando la lineal.
#aux = np.round(f_lineal(rango),5).tolist()
#
#print (aux.index (0.00001)) # Elemento mas chico antes de cambiar de signo la lineal.
#print (np.round(rango[aux.index (0.00001)],2)) # La temperatura con ese voltaje.

plt.title("Ajuste lineal cerca de 22.29 °C")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Voltaje (V)")
plt.grid()
plt.plot(x_4_temp,y_4_DAVS,".",color = "b")
plt.plot(x_4_temp[65:110],y_4_DAVS[65:110],".",color = "g")
plt.plot(rango,f_lineal(rango),color = "m")
#%%
# Guardo los parámetros de la lineal para ser utilizados en el lazo de control.

pendiente = a
ordenada = b
parametros = [pendiente,ordenada]
np.save("Param_Transf_Lineal_VoltajeTemperatura",parametros)