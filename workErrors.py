# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 21:47:43 2021

@author: anna-
"""

for i in range(0, len(noise)):    
    noise[i] = ec[i];   

r2= scipy.stats.pearsonr(noise, hours)
print(r2[0])


#0 godzin

for i in range(0, len(hours)):    
    y[i] = hours[i];   

# r2= scipy.stats.pearsonr(x[1:1100], y[1:1100]) #tylko z tej korzystam
r2= scipy.stats.pearsonr(x, y)
print(r2[0])


#0 dluzsze biomed.

for i in range(0, len(roomHumid)):    
    y[i] = roomHumid[i];   
r2= scipy.stats.pearsonr(x, y)
print(r2[0])
