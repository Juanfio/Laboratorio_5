# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:45:06 2019

@author: Publico
"""

import visa

rm = visa.ResourceManager()
tec = rm.open_resource('USB::0x1313::0x804A::M00404166::INSTR')

def temp_set(tec, temp):
        tec.write('SOUR2:TEMP {}C'.format(temp))
        
def temp_read(tec):
        temp = tec.query('SOUR2:TEMP?')
        print(temp)
        return(temp)
        