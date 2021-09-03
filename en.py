






for i in range(0, len(en)):    
    y[i] = en[i];   

r2= scipy.stats.pearsonr(x, y)
print(r2[0])

