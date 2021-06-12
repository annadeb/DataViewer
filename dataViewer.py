#from influxdb import InfluxDBClient

#client = InfluxDBClient(host='127.0.0.1', port=8086, database='painMonitor')


from influxdb import DataFrameClient

client = DataFrameClient(host='127.0.0.1', port=8086, username='root', password='root', database='painMonitor') 

dbs = client.get_list_measurements()
query='select * from sleepHours WHERE time < \'2021-06-11T08:00:28.000Z\' AND time > \'2021-05-01T06:09:15.000Z\''

series = client.query(query,method=u'GET')

print(series["sleepHours"])