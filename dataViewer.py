#from influxdb import InfluxDBClient

#client = InfluxDBClient(host='127.0.0.1', port=8086, database='painMonitor')


from influxdb import DataFrameClient
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

client = DataFrameClient(host='127.0.0.1', port=8086, username='root', password='root', database='painMonitor') 

dbs = client.get_list_measurements()
query='select * from roomTemp WHERE time > \'2021-05-17T06:09:15.000Z\' AND time < \'2021-05-17T18:00:28.000Z\''

series = client.query(query,method=u'GET')

print(series["roomTemp"])

#print(series["roomTemp"].values[0][0])
#print(series["roomTemp"].index[0])


plt.plot(series["roomTemp"].index,series["roomTemp"].values, '-', color='black');