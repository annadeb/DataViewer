





for i in range(0, len(ep)):    
    y[i] = ep[i]; 
 

    
r2= scipy.stats.pearsonr(x, y)
print(r2[0])
