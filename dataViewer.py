from influxdb import DataFrameClient
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd
import scipy.stats

startDate='2021-05-17T06:09:15.000Z'
endDate='2021-05-17T18:00:28.000Z'
measurment1= 'Hr'#'EDA_E4' #'roomCO2'#'Temperature
measurment2= 'roomTemp'#'nonPersErrorCount'#'roomPress' #'roomNoise' 
reject_values=False

if measurment1=='Hr' or measurment1=='EDA_E4':
    reject_values=True

client = DataFrameClient(host='127.0.0.1', port=8086, username='root', password='root', database='painMonitor') 

dbs = client.get_list_measurements()

#pierwsza zmienna
query='select * from ' + measurment1 + ' WHERE time > \'' + startDate + '\' AND time < \'' + endDate + '\''

series = client.query(query,method=u'GET')

#print(series[measurment1])

#print(series["roomTemp"].values[0][0])
#print(series["roomTemp"].index[0])

#plt.plot(series[measurment1].index,series[measurment1].values, '-', color='black');
new_series=series[measurment1].values
new_series_times=series[measurment1].index

#odrzut skrajnych wartosci - 5%
if reject_values:
    seriesvalues = series[measurment1].values.transpose()[0]
    number_largest = max(seriesvalues)
    number_smallest = min(seriesvalues)
    
    series_range = number_largest-number_smallest
    five_percent = 0.05*series_range
    fourty_percent = 0.4*series_range
    
    min_value_accept = number_smallest+five_percent
    max_value_accept = number_largest-fourty_percent
    
    new_series=[]
    new_series_times=[]
    iterate = 0
    for x in seriesvalues:
        if x <= min_value_accept:
            iterate = iterate+1
            continue
        if x>= max_value_accept:
            iterate = iterate+1
            continue
        new_series.append(seriesvalues[iterate])
        new_series_times.append(series[measurment1].index[iterate])
        iterate = iterate+1
    
    #plt.plot(new_series_times,new_series, '-', color='green');
    
#srednia kroczaca
df_series1 = pd.DataFrame(new_series, index =new_series_times)  
df_series1['average_series'] = df_series1.mean(axis=1)
    
df_series1['SMA_200'] = df_series1.average_series.rolling(200, min_periods=1).mean()
    
#plt.plot(df_series1['SMA_200'], '-', color='blue'); 

#druga zmienna
query2='select * from ' + measurment2 + ' WHERE time > \'' + startDate + '\' AND time < \'' + endDate + '\''
series2 = client.query(query2,method=u'GET')

#plt.plot(series2[measurment2].index,series2[measurment2].values, '-', color='red');

df_series2=pd.DataFrame(series2[measurment2].values, index =series2[measurment2].index.transpose())  

#resampling
series1_resampled = df_series1.resample('15S').bfill()
series2_resampled = df_series2.resample('15S').bfill()


series1_resampled['Series2']=series2_resampled

#korelacja
x = series1_resampled['SMA_200']#[0:1144]
y = series1_resampled['Series2']#[0:1144]
r = np.corrcoef(x, y)
#print(r[0, 1])
#print(r[1, 0])

r2= scipy.stats.pearsonr(x, y)
print(r2[0])
         
r3=scipy.stats.spearmanr(x, y)
print(r3[0])

r4=scipy.stats.kendalltau(x, y)
print(r4[0])

plt.plot(x, '-', color='blue'); 
plt.plot(y, '-', color='green'); 
