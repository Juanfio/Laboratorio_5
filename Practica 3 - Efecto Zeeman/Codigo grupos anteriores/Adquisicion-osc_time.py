import visa
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time

from instrumentos import Osciloscopio

osci = Osciloscopio('USB::0x0699::0x0363::C102223::INSTR') #Cambia con el osc
#%%

control = True
t0 = time.perf_counter()
TrefRub = 

while control == True:
    print('start loop')
    tiempo1, data1 = osci.get_ventana(1)
    tiempo2, data2 = osci.get_ventana(2)
    ch1 = np.array([tiempo1, data1])
    ch2 = np.array([tiempo2, data2])
    #measurement_name = 'Tref'+str(datetime.datetime.now().hour)+'_'+str(datetime.datetime.now().minute)+'_'+str(datetime.datetime.now().second)
    measurement_name = str(TrefRub+str(datetime.datetime.now().hour)+'_'+str(datetime.datetime.now().minute)+'_'+str(datetime.datetime.now().second)
    print('plotting')
    plt.figure(2)
    plt.title('Voltaje vs Tiempo', size = 16)
    plt.plot(tiempo1,data1,'r*-', markersize=1,label='CH1')
    plt.plot(tiempo2,data2,'b*-', markersize=1, label='CH2')
    plt.xlabel('Tiempo[ms]', size=12)
    plt.ylabel('Voltaje[mV]', size=12)
    plt.legend()
    plt.show()
    print('saving')
    np.save('canal1_'+measurement_name, ch1)
    np.save('canal2_'+measurement_name, ch2)
    plt.pause(5)
    plt.close()      
    t1 = time.perf_counter()
    
    if t1-t0 > 20:
        control = False
    print('end loop')