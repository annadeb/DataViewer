





for i in range(0, len(ec)):    
    y[i] = ec[i];   


r2= scipy.stats.pearsonr(x, y)
print(r2[0])



