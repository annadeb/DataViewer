#from influxdb import InfluxDBClient

#client = InfluxDBClient(host='127.0.0.1', port=8086, database='painMonitor')


from influxdb import DataFrameClient
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd

startDate='2021-05-17T06:09:15.000Z'
endDate='2021-05-17T18:00:28.000Z'
measurment1='Hr' #'roomTemp';
measurment2='Temperature';

client = DataFrameClient(host='127.0.0.1', port=8086, username='root', password='root', database='painMonitor') 

dbs = client.get_list_measurements()
query='select * from ' + measurment1 + ' WHERE time > \'' + startDate + '\' AND time < \'' + endDate + '\''

series = client.query(query,method=u'GET')

#print(series[measurment1])

#print(series["roomTemp"].values[0][0])
#print(series["roomTemp"].index[0])

plt.plot(series[measurment1].index,series[measurment1].values, '-', color='black');


#odrzut skrajnych wartosci - 5%
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

plt.plot(new_series_times,new_series, '-', color='green');

#srednia kroczaca
df_series = pd.DataFrame(new_series, index =new_series_times)  
df_series['average_series'] = df_series.mean(axis=1)

df_series['SMA_10'] = df_series.average_series.rolling(200, min_periods=1).mean()

plt.plot(new_series_times,df_series['SMA_10'], '-', color='blue'); 

#query2='select * from ' + measurment2 + ' WHERE time > \'' + startDate + '\' AND time < \'' + endDate + '\''
#series2 = client.query(query2,method=u'GET')

#series2time = pd.Series(series2[measurment2].index.transpose(),series2[measurment2].values.transpose())
#series2time.resmple('20S')

#plt.plot(series2[measurment2].index,series2[measurment2].values, '-', color='blue');

#iterator = 0
#arrayElement=0
#series2resampled = [];
#for x in series2[measurment2].values:
#  if iterator%70==0:
#      series2resampled.append(series2[measurment2].values[iterator][0])
#      arrayElement=arrayElement+1
#  iterator=iterator+1
  

  