from pprint import pprint
import requests
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Clarksville&units=metric&APPID=301e59e1ab9370e1f7644445df46f156')
pprint(r.json())
