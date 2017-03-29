# GUI for Smart MIRROR
# Currently includes:
# - Title
# - Digital Clock that updates every 200ms
# - Weather Information
# - Most recent tweet from POTUS
# - Greeting Daytime

from Tkinter import *
import time
import requests
import tweepy
import datetime
import xmltodict

fonttype = 'adobe' # different maybe franklin
fontstyle = 'bold'

###################################################
# Functions to be repeated and updated while running
def clockUpdate():
    global time1
    today = datetime.date.today()

    time2 = time.strftime('%H:%M:%S')
    time2 = time2 + '\n'+str(today)

    if time2 != time1:
        time1 = time2
        Clock.config(text=time2)

    timeOfDay()
    Clock.after(200, clockUpdate)

def stockAPICall():
    url1 = "http://dev.markitondemand.com/MODApis/Api/v2/Quote"
    parameters = {'symbol':"AAPL", 'callback':"jsoncallback"}
    stock = requests.get(url1, params=parameters)
    if stock.status_code == 200:
        data1 = xmltodict.parse(stock.content)

    print data1
    stockData.config(text = "Stock: " + data1[u'StockQuote'][u'Name']
                            +"\nStock Price: " + data1[u'StockQuote'][u'LastPrice'])


def weatherAPICall():
    url = 'http://api.openweathermap.org/data/2.5/weather?APPID=301e59e1ab9370e1f7644445df46f156' # url goes here
    location = 'Clarksville' # adjust as required
    unit = 'metric'
    paramaters = {'q':location, 'units':unit}
    response = requests.get(url, params = paramaters)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Something went wrong')

    print data
    t = u"\u00b0"
    WeatherTemp.config(text = data[u'weather'][0][u'description']
                        + '\nTemperature: '
                        + str(data[u'main'][u'temp'])
                        + t + 'C')

def twitterAPICall():
    consumer_key= '5Sgpga1fHgZ9IxAC5oKMXdHod'
    consumer_secret= 'fU4DN8njObtDCFnr6gYMo03e40O53iJQ2VDdzOP89zuMabJfFJ'
    access_token='3783517036-bA3q6lemHcLgu9QFOX0FJMoqUYR1UPLlaNKQO0g'
    access_token_secret='CEguhLq6UtHzUw304tzjM4iO3WhgkmUfDyAeMhEn19Xhn'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    potus_tweet = api.user_timeline(screen_name = 'potus',count=2)
    print potus_tweet[0].text
    PotusTweet.config(text = potus_tweet[0].text)

def timeOfDay():
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:
        DayGreet.config(text = 'Good Morning Handsome')
    elif 12 <= currentTime.hour < 18:
        DayGreet.config(text = 'Good Afternoon \nHandsome')
    else:
        DayGreet.config(text = 'Good Evening Handsome')

###################################################




###################################################
# Initializing root. Main GUI Object Window
root = Tk()
###################################################



###################################################
# Clock Object
time1 = ''
Clock = Label(root, font=(fonttype, 40, fontstyle), bg='black',fg='white')
Clock.pack(side=LEFT,expand=0)

# Weather Object
WeatherTemp = Label(root, font=(fonttype,40,fontstyle),bg='black',fg= 'white')
WeatherTemp.pack(side = RIGHT, expand =0)

#Stock Object
stockData = Label(root, font=(fonttype,40,fontstyle),bg='black',fg= 'white')
stockData.pack(side = RIGHT, expand =0)
stockData.place(x=900, y=400)

# Title Object
Title = Label(root, font=(fonttype, 80, fontstyle), bg='black',fg='white')
Title.pack(side=TOP,expand=0)
#Title.config(text = 'SMART MIRROR')

# Greeting Object
DayGreet = Label(root, font=(fonttype, 65, fontstyle), bg='black',fg='white')
DayGreet.pack(side=TOP,expand=0)

#Footer
Title = Label(root, font=(fonttype,20, fontstyle), bg='black',fg='white')
Title.pack(side=BOTTOM,expand=0)
Title.config(text = 'Project by Group 1: \nDominic Critchlow, Travis Hodge, Dylan Kellogg, Michael Timbes')

# POTUS Twitter
PotusTweet = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= 'white')
PotusTweet.pack(expand = 0)
###################################################




###################################################
# Call Function for items
clockUpdate()
weatherAPICall()
twitterAPICall()
stockAPICall()
#timeOfDay()
###################################################




###################################################
# Main structure of window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.configure(background='black')
# Running of the GUI Loop
root.mainloop(  )
###################################################
