import numpy as np
import matplotlib.pyplot as plt
numberOfFiles = 120 #numero de archivos
i = 1
volt = []
temp = []
while i <= numberOfFiles:    
    volt_total = np.load('volt_ch2_'+str(i)+'.npy')
    volt_total = volt_total[1, :]
    volt = np.append(volt, np.mean(volt_total))
    temp = np.append(temp, np.load('temp'+str(i)+'.npy'))
    i = i + 1
#%%
plt.figure(3)
plt.plot(temp,volt,'.')
plt.grid()
plt.show()
#%%
import numpy as np
import matplotlib.pyplot as plt
numberOfFiles = 47 #numero de archivos
i = 1
j = 1
volt_ch1 = []
volt_ch2 = []
temp = []
while i <= numberOfFiles:    
    volt_total_ch1 = np.load('volt_ch1_'+str(i)+'.npy')
    volt_total_ch1 = volt_total_ch1[0, :]
    volt_ch1 = np.append(volt_ch1, np.mean(volt_total_ch1))
    i = i + 1
#while j <= numberOfFiles:    
#    volt_total_ch2 = np.load('volt_ch2_'+str(j)+'.npy')
#    volt_total_ch2 = volt_total_ch2[0, :]
#    volt_ch2 = np.append(volt_ch2, np.mean(volt_total_ch2))
#    j = j + 1

temp = np.load('temp47.npy')
#%%
plt.figure(1)
#plt.plot(temp,volt_ch1,'r.')
plt.plot(temp,volt_ch2,'b.')
plt.show()
#%%
import numpy as np
import matplotlib.pyplot as plt
number_of_files = 47
i=1
j=1
volt_ch1 = []
volt_ch2 = []
temp = []
#%%
plt.plot(volt[0,:],volt[1,:])
plt.show()