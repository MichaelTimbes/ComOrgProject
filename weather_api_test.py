import requests

url = 'http://api.openweathermap.org/data/2.5/weather?APPID=301e59e1ab9370e1f7644445df46f156' # url goes here
location = 'Clarksville' # adjust as required
unit = 'metric'
paramaters = {'q':location, 'units':unit}
response = requests.get(url, params = paramaters)
if response.status_code == 200:
    data = response.json()
else:
    print('Something went wrong')

print data #data[u'weather'][0][u'description'] #adressing data from the set
