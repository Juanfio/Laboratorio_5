# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:52:38 2019

@author: juan
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import stats
import math
from decimal import Decimal
#%%
def as_si(x, ndp):
    s = '{x:0.{ndp:d}e}'.format(x=x, ndp=ndp)
    m, e = s.split('e')
    return r'{m:s}\times 10^{{{e:d}}}'.format(m=m, e=int(e))
#%% Esto es solamente para ver como se ven el set de datos graficado.
barrido_3 = np.load ("13.BarridoTempDAVS_22.50_23.12.npy")
barrido_4 = np.load ("14.BarridoTempDAVS_22.90_23.025.npy")

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
barrido_4 = np.load ("14.BarridoTempDAVS_22.90_23.025.npy")

x_4_temp = []
y_4_DAVS = []

for i in range (len(barrido_4)):
    x_4_temp.append(np.round(barrido_4[i][3],5))
    y_4_DAVS.append(barrido_4[i][2]-0.020)
#print (x_4_temp.index(22.98))

# Pendiente de la recta, ordenada al origen y matriz de covarianza.
# La pendiente depende del rango de valores en los cuales realizo el ajuste lineal.
# Por ejemplo: x_4_temp[93:100] en este rango de temperaturas es bastante pronunciada la pendiente.
POC = np.polyfit (x_4_temp[22:40],y_4_DAVS[22:40],1,cov=True) 
# Varianza de los parametros.
var_pendiente = POC[1][0][0]
var_ordenada = POC[1][1][1]

a = POC[0][0]
b = POC[0][1]
f_lineal = lambda x: a*x+b

# Para el ploteo de la lineal.
rango = np.linspace (min (x_4_temp[22:37]),max (x_4_temp[22:37]),1000)

# Para hallar la temperatura donde es cero el voltaje, utilizando la lineal.
aux = np.round(f_lineal(rango),5).tolist()

#print (aux.index (0.00002)) # Elemento mas chico antes de cambiar de signo la lineal.
#print (rango[aux.index (0.00002)]) # La temperatura con ese voltaje.
#
#print (a,b)
plt.title("Ajuste lineal cerca de 22.96 °C")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Voltaje (V)")
plt.grid()
#textstr = '\n'.join((
#    r'$a=%.2f$' % (a, ), #El subindice 5 indica que es el de la curva del punto 5.
#    r'$b=%.2f$' % (b, )))
#print(math.sqrt(var_pendiente))
#print(math.sqrt(var_ordenada))
textstr = "a = -0.856" u"\u00B1" "0.087" "\n" "b = 19.67" u"\u00B1" "1.99"
           
plt.text(22.90, 0.015, textstr, fontsize=10, verticalalignment='top')
plt.plot(x_4_temp,y_4_DAVS,".",color = "b")
plt.plot(x_4_temp[22:40],y_4_DAVS[22:40],".",color = "g")
plt.plot(rango,f_lineal(rango),color = "m")
#%%
# Guardo los parámetros de la lineal para ser utilizados en el lazo de control.
pendiente = a
ordenada = b
parametros = [pendiente,ordenada]
np.save("Param_Transf_Lineal_VoltajeTemperatura",parametros)

#%% Analisis de los datos guardados en el archivo del lazo de control.
data_1 = np.load("2.Lazo.npy")
volt_davs_1 = []
tiempo_1 = []
temperatura_1 = [] # Temperatura leida por el ITC.
parametros_lazo_1 = data_1[-1]
rango_error = 0.01
for i in range(len(data_1)-1):
    volt_davs_1.append(data_1[i][2]-data_1[i][3]-0.020)
    tiempo_1.append(data_1[i][4])
    temperatura_1.append(data_1[i][1])

delta_T_1 = '%.2E' % Decimal(max(temperatura)-min(temperatura))
plt.title("Evolución temporal de la señal DAVS" "\n" "con el lazo de control")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.hlines(0.01,0,max(tiempo_1),linestyles = 'dashed',color = "m")
#plt.hlines(-0.01,min(tiempo_1),max(tiempo_1),linestyles = 'dashed',color = "m")
plt.grid()
plt.plot(tiempo_1,volt_davs_1,".",color = "b")


data_2 = np.load("3.Lazo.npy")
volt_davs_2 = []
tiempo_2 = []
temperatura_2 = [] # Temperatura leida por el ITC.
parametros_lazo_2 = data_2[-1]
for i in range(len(data_2)-1):
    volt_davs_2.append(data_2[i][2]-data_2[i][3]-0.020)
    tiempo_2.append(data_2[i][4])
    temperatura_2.append(data_2[i][1])

delta_T_2 = '%.2E' % Decimal(max(temperatura_2)-min(temperatura_2))

print (delta_T_1)
a = 7.63e-4
Kp_1 = 1.96
Ki_1 = 0.76
textstr_1 = '\n'.join((
    r'$Kp=%.2f$' % (Kp_1, ), #El subindice 5 indica que es el de la curva del punto 5.
    r'$Ki=%.2f$' % (Ki_1, )))

print (delta_T_2)
b = 1.01e-3
Kp_2 = 2.96
Ki_2 = 0.50
textstr_2 = '\n'.join((
    r'$Kp=%.2f$' % (Kp_2, ), #El subindice 5 indica que es el de la curva del punto 5.
    r'$Ki=%.2f$' % (Ki_2, )))

plt.text(400, 0.025," ".join((r"$\Delta T= {0:s}$".format(as_si(a,2)),"°C")), fontsize=9, verticalalignment='top',color="b")
plt.text(400, 0.023,textstr_1 , fontsize=9, verticalalignment='top',color="b")
plt.text(400, 0.019," ".join((r"$\Delta T= {0:s}$".format(as_si(b,2)),"°C")), fontsize=9, verticalalignment='top',color="r")
plt.text(400, 0.017,textstr_2 , fontsize=9, verticalalignment='top',color="r")
plt.plot(tiempo_2,volt_davs_2,".",color = "r")
plt.show()




