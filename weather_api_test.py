import requests
import time


description = []
time_write = 0
thefile = open('weather_descriptions.txt', 'a')

while True:
    time.sleep(5)
    time_write += 1
    url = 'http://api.openweathermap.org/data/2.5/weather?APPID=301e59e1ab9370e1f7644445df46f156' # url goes here
    location = 'Clarksville' # adjust as required
    unit = 'metric'
    paramaters = {'q':location, 'units':unit}
    response = requests.get(url, params = paramaters)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Something went wrong')

    print (data)


    print("weatherImages/" + data[u'weather'][0][u'description'] + ".png")

    if data[u'weather'][0][u'description'] not in description:
        description.append(data[u'weather'][0][u'description'])


    if time_write > 500 :
        time_write =0
        description.write("\n" )
        for item in description:
            thefile.write("%s " % item)
