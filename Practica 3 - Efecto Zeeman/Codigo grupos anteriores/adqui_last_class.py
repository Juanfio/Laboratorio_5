#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:48:36 2019

@author: jlaurna
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
v0 #A determinar de estudiar la DAVS barrida en T
deltaT = 0.0 #A pensar 

while True:
    T = temp_read(tec)
    temp = np.array(T)
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    ch1 = np.array([tiempo1, data1])
    ch2 = np.array([tiempo2, data2])
    measurement_name = str(i)
    np.save('temp'+measurement_name, temp)
    np.save('volt_ch1_'+measurement_name, ch1)
    np.save('volt_ch2_'+measurement_name, ch2)
    
    #El P no deberia ejecutarse en cada instancia de levantar datos. Hay que considerar un tiempo de acomodamiento del sistema una vez que se le modifica la temperatura. Pensamos que si e tiempo de acomodamiento es del orden de un numero "entero" de veces el tiempo en el que medimos podemos hacer un contador aparte de ese numero de veces.
    if v > v0:
        temp_set(tec, T + deltaT)
    elif v < v0:
        temp_set(tec, T - deltaT)
    
    i = i + 1
    #plt.pause(60) #A pensar
    
