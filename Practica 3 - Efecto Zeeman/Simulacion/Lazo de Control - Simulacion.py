# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:42:43 2019

@author: Publico
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import datetime
#from control import ITC4001
import scipy as sp
from scipy import stats
import random as rm
from decimal import Decimal
#%%
def as_si(x, ndp):
    s = '{x:0.{ndp:d}e}'.format(x=x, ndp=ndp)
    m, e = s.split('e')
    return r'{m:s}\times 10^{{{e:d}}}'.format(m=m, e=int(e))
#%%
# Cargo la funcion lineal que transforma voltaje en temperatura.
parametros_VoltajeVsTemp = np.load ("Param_Transf_Lineal_VoltajeTemperatura.npy")
a = parametros_VoltajeVsTemp[0]
b = parametros_VoltajeVsTemp[1]
f_volt_temp = lambda x: a*x+b # Esta funcion transforma temperaturas a voltajes.

# Esto transforma temperaturas (x) a Voltaje (f(x)). Vamos a invertirla.
f_temp_volt = lambda y: (y-b)/a # Esta funcion transforma voltajes a temperatura.
print(round(f_volt_temp(22.9630),3))
#%%
# Tener en cuenta:
#1. Tengo que generar una variable aleatoria (voltaje) entre el rango de voltajes que medimos nosotros. 
#2. No me tengo que pasar de la temperatura en donde nuestro ajuste lineal funciona.
#3. Ver si tiene sentido la "correccion" de la temperatura en el lazo simulado. Por ahi directamente se puede guardar
#en alguna variable las temperaturas corregidas.
#4. Importante: Ver como asociamos que una dada temperatura (ejemplo T0 = 22.964) esta asociada al voltaje cero.
#Supongo yo que con la lineal.
#5.Que el voltaje fluctue significa que la temperatura esta cambiando, y cuando el lazo tiene que corregir no es el mismo
#tiempo el que le toma corregir 0.001 grados que corregir 0.1 grados. Asociamos 0.01° == 1segundo.
#Importante (5): Si dejo que el lazo antes de activarse tarde el tiempo necesario para corregir bien la temperatura 
#entonces no tienen sentido los parametros Kp y Ki, el objetivo es que estos corrijan lo mejor posible la T.
# El problema central: Darle un tiempo antes de que vuelva a correr es para que el ITC logre corregir su temperatura.

#Si yo asumo que le toma 0.5 segundo corregir 0.001°. Si quiero dejar un intervalo de 10 segundos entre cada vuelta del
lazo, tengo que hacer (10 s * 0.001 °)/0.5 s --> esto representa la cantidad de grados que corrigio en ese tiempo.
#%%
# Condiciones iniciales.
V0 = 0 # Voltaje de setpoint.
voltaje_corregido = V0
T0 = 22.964
t_corregida = T0
t_loop = 0
respuesta_lazo = 3
temp_por_segundo = 0.002 #(cuantos grados corrige por segundo)
voltajeDAVS_final = 0
N = 15

e_t = []
T_loop = []
K_p = 1.90
K_i = 0.5
rango_error = 0.2 #Da cuenta de la sensibilidad del lazo.
datos_guardados = []

# Transformación lineal que me da la cantidad de segundos que le toma al aparato corregir la temperatura.
# Respuesta lazo tenemos que poner el tiempo de espera antes de corer el loop.

while t_loop < 1000: # Vamos a hacer una medicion en donde el lazo funciona durante 10
                    # minutos. t_loop guarda la evolucion temporal al sumar 30 segundos
                    # en cada iteracion.
#    voltaje1 = rm.uniform(-0.040,0.040)
#    voltaje2 = rm.uniform(-0.040,0.040)
    # Genero variables aleatorias con un 68% de probabilidad de estar contenida en el intervalo de error.        
    grados = respuesta_lazo*temp_por_segundo
    for i in range (N):
        voltajeDAVS = np.random.normal(loc = voltajeDAVS_final, scale = 0.1)
#        voltajeDAVS = np.random.normal(loc = 0, scale = 0.1)
#       voltajeDAVS = rm.uniform(-0.400,0.400)    
    e_t.append(V0 - voltajeDAVS) 
    T_loop.append(t_loop)
    e_t_i = sp.integrate.simps(e_t,T_loop)
    e_t_p = V0 - voltajeDAVS
    
    voltaje_corregido = voltaje_corregido + K_p * e_t_p + K_i * e_t_i
    
    if abs(e_t_p) > rango_error: #Correccion a lo anterior: Tomamos el valor absoluto de la señal error.
       
        # cantidad de grados que logra corregir en ese intervalo de tiempo.
        
        # temperatura en 
        t_seteada = f_temp_volt (voltaje_corregido)
        if t_seteada > t_corregida:
            t_corregida = t_corregida + grados
        elif t_seteada <= t_corregida:
            t_corregida = t_corregida - grados
            
    t_corregida = t_corregida + np.random.normal(0,0.01) #le ponemos un poquito de ruido a la temperatura.
    
    voltajeDAVS_final = f_volt_temp(t_corregida) + np.random.normal(0,0.1)
#    print ([voltajeDAVS,voltaje_corregido,f_temp_volt (voltaje_corregido),voltajeDAVS_final])
    
    t_loop = t_loop + respuesta_lazo
    
    # Informacion guardada de cada ajuste del lazo: temperatura_corregida, temperatura que
    # lee el ITC, y los voltajes.
    # Vuelvo a leer los voltajes luego de ajustar la temperatura.
    
    datos_guardados.append([t_corregida,voltajeDAVS_final,t_loop,voltajeDAVS])
    
datos_guardados.append ([K_p,K_i])
data_1 = datos_guardados
#%%
np.save("14.Lazo_simulacion",datos_guardados)
#%%
# En 12,13,14 el rango error es 0.2.
#data_1 = np.load("14.Lazo_simulacion.npy")
volt_davs_1 = []
tiempo_1 = []
temperatura_1 = [] # Temperatura leida por el ITC.
parametros_lazo_1 = data_1[-1]
#rango_error = 0.01
for i in range(len(data_1)-1):
    volt_davs_1.append(data_1[i][1])
    tiempo_1.append(data_1[i][2])
    temperatura_1.append(data_1[i][0])

textstr_1 = '\n'.join((
    r'$Kp=%.2f$' % (parametros_lazo_1[0], ), #El subindice 5 indica que es el de la curva del punto 5.
    r'$Ki=%.2f$' % (parametros_lazo_1[1], )))

print('%.2E' % Decimal(max(temperatura_1)-min(temperatura_1)))
#print(parametros_lazo_1)
a = 4.5e-01
plt.title("Evolución temporal de la señal DAVS" "\n" "con el lazo de control (Simulación)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.hlines(rango_error,0,max(tiempo_1),linestyles = 'dashed',color = "m")
plt.hlines(-rango_error,0,max(tiempo_1),linestyles = 'dashed',color = "m")
#
plt.text(0, -0.30," ".join((r"$\Delta T= {0:s}$".format(as_si(a,2)),"°C")), fontsize=10, verticalalignment='top',color="b")
plt.text(0, -0.22,textstr_1 , fontsize=9, verticalalignment='top',color="b")
plt.grid()
plt.plot(tiempo_1,volt_davs_1,".",color = "b")
plt.show()
#print (parametros_lazo_1)
#%%
print(temperatura_1)
#print(np.random.normal(0,0.1))


#%%
Cosas importantes lazo:

1. Distribucion normal cerca del cero.
2. No se lograba corregir toda la temperatura sino la cantidad de grados dada por el tiempo que corriamos.
#%%
Comunicar sobre el lazo simulado:
*. Nosotros cuando hicimos el lazo lo que habiamos hecho era que esperara 10 segundos antes de volver a correrse, 
y que en esos 10 segundos el ITC fuera a la temperatura seteada. En la simulación eso se representaba seteando la 
temperatura final en aquella alcanzada luego de pasar 10 segundos, bajo la hipotesis de que cada 1 segundo se 
corrigen 0.002 grados. (Asumimos que al dispositivo le toma 0.5 segundos corregir 0.001 grados)

*. Si el voltaje corregido al ser colocado en la transformacion lineal que define la temperatura a la cual seteamos el
ITC, da una temperatura mayor a T0 entonces la cantidad de grados que podemos corregir en esos 10 segundos los sumamos
a T0 (porque queremos ir para arriba con la T); caso contrario lo restamos. Importante: la temperatura final no es la que
define ese voltaje corregido sino T0 + grados (si habia que subir la T) o T0 - grados (si habia que bajarla).

*. Fenómeno real: Seteabamos la temperatura en aquella que hacia que el voltaje fuera cero. Pero cuando mediamos si este
se habia corrido hacia arriba el lazo buscaba corregir la temperatura para hacer bajar ese valor de voltaje.
Suponiendo que lo hacia bajar un poco pero no llegaba a cero, al momento de volver a correr el lazo la señal real 
fisica habia fluctuado alrededor de ese valor de voltaje nuevo. Eso lo simulabamos con la variable aleatoria con
distribucion gaussiana alrededor del voltaje que se obtenia producto de esta nueva temperatura.

*. Despues de corregir la temperatura, redefinimos el voltaje de la DAVS utilizando la transformacion lineal
y eso es lo que guardamos. Esta parte de la simulacion representa lo que en nuestro lazo haciamos al final, que era 
guardar el valor que leia de voltaje el osciloscopio luego de haber seteado una nueva temperatura.
