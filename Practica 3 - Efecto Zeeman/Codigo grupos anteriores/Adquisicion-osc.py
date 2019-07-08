import visa
import matplotlib.pyplot as plt
import numpy as np
import datetime

from instrumentos import Osciloscopio

osci = Osciloscopio('USB::0x0699::0x0363::C102220::INSTR')
#%%
tiempo1, data1 = osci.get_ventana(1)
tiempo2, data2 = osci.get_ventana(2)

plt.figure(1)
plt.title('Voltaje vs Tiempo', size = 16)
plt.plot(tiempo1,data1,'r*-', markersize=1,label='CH1')
plt.plot(tiempo2,data2,'b*-', markersize=1, label='CH2')
plt.xlabel('Tiempo[ms]', size=12)
plt.ylabel('Voltaje[mV]', size=12)
plt.legend()  
plt.show()
#%%
ch1 = np.array([tiempo1, data1])
ch2 = np.array([tiempo2, data2])
measurement_name = 'Tref'+str(datetime.datetime.now().hour)+'_'+str(datetime.datetime.now().minute)
np.save('canal1_'+measurement_name, ch1)
np.save('canal2_'+measurement_name, ch2)