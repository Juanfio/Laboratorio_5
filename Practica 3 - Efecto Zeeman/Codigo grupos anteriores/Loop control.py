import numpy as np
import time
import matplotlib.pyplot as plt
import datetime
from control import ITC4001

itc = ITC4001('USB::0x1313::0x804A::M00404166::INSTR')

#%%
temp_set = itc.temperature_setpoint(22.5)
curr_set = itc.current_setpoint(0.0014)

error = []

P = 10
I = 0
D = 0

integral = 0

while True:
    temp_read = itc.measurement()
    e = temp_set - temp_read
    error.append(e)
    if len(error) == 10:
        error.pop(0)
        integral = np.mean(error)
    if abs(e)>0.001:
        temp_set = temp_set + P*e + I*integral #+ D*derivada
    
    time.sleep(2)

#%