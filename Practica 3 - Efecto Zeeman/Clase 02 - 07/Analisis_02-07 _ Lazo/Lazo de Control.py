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

#%%
# Cargo la funcion lineal que transforma voltaje en temperatura.
parametros_VoltajeVsTemp = np.load ("Param_Transf_Lineal_VoltajeTemperatura.npy")
a = parametros_VoltajeVsTemp[0]
b = parametros_VoltajeVsTemp[1]
f_lineal = lambda x: a*x+b

# Esto transforma temperaturas (x) a Voltaje (f(x)). Vamos a invertirla.
f_temp_volt = lambda y: (y-b)/a # Esta funcion transforma voltajes a temperatura.
#%%
# Condiciones iniciales.
V0 = 0 # Voltaje de setpoint.
t_loop = 0
respuesta_lazo = 2
voltaje_corregido = V0
#Al definirlo aca le seteamos tambien la temperatura inicial.
T0 = 22.964
temperatura_corregida = T0
temp_set(tec,T0) 

e_t = []
T_loop = []
K_p = 2.96
K_i = 0.50
rango_error = 0.01 #Da cuenta de la sensibilidad del lazo.
datos_guardados = []

# Respuesta lazo tenemos que poner el tiempo de espera antes de corer el loop.
while t_loop < 600: # Vamos a hacer una medicion en donde el lazo funciona durante 10
                    # minutos. t_loop guarda la evolucion temporal al sumar 30 segundos
                    # en cada iteracion.
    tiempo1, voltaje1 = osci.get_ventana(1)
    tiempo2, voltaje2 = osci.get_ventana(2)
    
    voltaje1 = np.mean(voltaje1)
    voltaje2 = np.mean(voltaje2)
    
    voltajeDAVS = voltaje1 - voltaje2
    
    e_t.append(V0 - voltajeDAVS) 
    T_loop.append(t_loop)
    e_t_i = sp.integrate.simps(e_t,T_loop)
    e_t_p = V0 - voltajeDAVS
    
    voltaje_corregido = voltaje_corregido + K_p * e_t_p + K_i * e_t_i
    
    if e_t_p > rango_error:
    # Hay que convertir con la relacion lineal de Voltaje vs Temperatura que se obtiene en
    # un entorno del cero de la DAVS, este voltaje_corregido a temperatura_corregida.        
        
        temperatura_corregida = f_temp_volt (voltaje_corregido)
        temp_set(tec, temperatura_corregida)
        
    # En caso de que e_t_p sea menor a ese valor definido, no resulta necesario corregir
    # la temperatura.
    
    t_loop = t_loop + respuesta_lazo
    
    # Informacion guardada de cada ajuste del lazo: temperatura_corregida, temperatura que
    # lee el ITC, y los voltajes.
    # Vuelvo a leer los voltajes luego de ajustar la temperatura.
    tiempo1, voltaje1 = osci.get_ventana(1)
    tiempo2, voltaje2 = osci.get_ventana(2)
    
    voltaje1 = np.mean(voltaje1)
    voltaje2 = np.mean(voltaje2)
    
    datos_guardados.append([temperatura_corregida,temp_read(tec),voltaje1,voltaje2,t_loop])
    
    time.sleep(respuesta_lazo)
    print (t_loop)
    
datos_guardados.append ([K_p,K_i])
#np.save("3.Lazo",datos_guardados)