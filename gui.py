# GUI for Smart MIRROR
# Currently includes:
# - Title
# - Digital Clock that updates every 200ms
# - Weather Information
# - Most recent tweet from POTUS
# - Greeting Daytime
from __future__ import print_function
from Tkinter import *
import time
import requests
import tweepy
import datetime
import xmltodict
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from PIL import Image, ImageTk

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES_cal = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE_cal = 'client_secret.json'
APPLICATION_NAME_cal = 'Google Calendar API Python Quickstart'

SCOPES_gmail = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE_gmail = 'client_secret.json'
APPLICATION_NAME_gmail = 'Gmail API Python Quickstart'


fonttype = 'adobe' # different maybe franklin, need to check with good fonts on Rasbian
fontstyle = 'bold'
foreground = 'white'

def exit():
    root.quit()

def get_credentials_calendar():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_cal, SCOPES_cal)
        flow.user_agent = APPLICATION_NAME_cal
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_credentials_gmail():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_gmail, SCOPES_gmail)
        flow.user_agent = APPLICATION_NAME_gmail
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

###################################################
# Functions to be repeated and updated while running


def clockUpdate():
    global time1
    today = datetime.date.today()
    time2 = time.strftime('%H:%M:%S')
    time2 = time2 + '\n'+str(today.strftime("%A \n%d %B %Y"))

    if time2 != time1:
        time1 = time2
        Clock.config(text=time2)

    timeOfDay()
    Clock.after(200, clockUpdate)

def timeOfDay():
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:
        DayGreet.config(text = 'Good Morning')
    elif 12 <= currentTime.hour < 18:
        DayGreet.config(text = 'Good Afternoon')
    else:
        DayGreet.config(text = 'Good Evening')

def stockAPICall():
    url1 = "http://dev.markitondemand.com/MODApis/Api/v2/Quote"
    parameters = {'symbol':"AAPL", 'callback':"jsoncallback"}
    stock = requests.get(url1, params=parameters)
    if stock.status_code == 200:
        stock_json = xmltodict.parse(stock.content)
    print (stock_json)
    StockData.config(text = "Stock: " + stock_json[u'StockQuote'][u'Name']
                            +"\nStock Price: " + stock_json[u'StockQuote'][u'LastPrice'])

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

    print (data)
    t = u"\u00b0"

    print("weatherImages/" + data[u'weather'][0][u'description'] + ".png")

    # Image include with resizing
    displayWeatherImage(data[u'weather'][0][u'description'])


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

    potus_tweet = api.user_timeline(screen_name = 'cnnbrk',count=2)
    result_tweet = potus_tweet[0].text
    #result_tweet = result_tweet.sub(r"http\S+", "", subject)
    print (result_tweet)
    PotusTweet.config(text = result_tweet)

def calendarAPICall():

    credentials = get_credentials_calendar()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print (now)
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
        CalenderLabel.config(text = 'No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            CalenderLabel.config(text = events[0]['start'].get('dateTime', events[0]['start'].get('date'))+ " " + events[0]['summary'])

def gmailAPICall():
    credentials = get_credentials_gmail()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results1 = service.users().messages().list(userId = 'me', q = 'is:unread',maxResults = 5).execute()
    unread_mes_num = results1.get(u'resultSizeEstimate')
    unread_mes_id = results1.get(u'messages',[])
    print ("number of message: " + str(unread_mes_num) + '\n ')
    print (unread_mes_id)

    subject = [None]*10
    i=0
    if unread_mes_num == 0:
        print("No unread Messages!")
        GmailLabel.config(text="No unread Messages!")

    else:
        for unreads in unread_mes_id:
            message1 = service.users().messages().get(userId='me', id=unreads[u'id'], format='metadata').execute()
            msg = message1[u'payload']

            for header in msg[u'headers']:
                if header[u'name'] == u'Subject':
                    subject[i] = header[u'value']
                    break
            if subject:
                print (subject)
            i += 1
        GmailLabel.config(text=(subject[0] + "\n"))

def displayWeatherImage(description):

    image = Image.open("weatherImages/" + "sunny" + ".png")
    image = image.resize((270, 250), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    WeatherImage.configure(image=photo)
    WeatherImage.image = photo

#sunny ->  image = image.resize((270, 250), Image.ANTIALIAS)



###################################################



###################################################
# Initializing root. Main GUI Object Window
root = Tk()
###################################################



###################################################
# Clock Object
time1 = ''
Clock = Label(root, font=(fonttype, 40, fontstyle), bg='black',fg=foreground)
Clock.pack(side=LEFT,expand=0)

# Weather Object
WeatherTemp = Label(root, font=(fonttype,40,fontstyle),bg='black',fg= foreground)
WeatherTemp.pack(side = RIGHT, expand =0)

# Stock Object
StockData = Label(root, font=(fonttype,40,fontstyle),bg='black',fg= foreground)
StockData.pack(side = RIGHT, expand =0)
StockData.place(x=900, y=700)

# Title Object
Title = Label(root, font=(fonttype, 80, fontstyle), bg='black',fg=foreground)
Title.pack(side=TOP,expand=0)

# Greeting Object
DayGreet = Label(root, font=(fonttype, 65, fontstyle), bg='black',fg=foreground)
DayGreet.pack(side=TOP,expand=0)

# Footer
Title = Label(root, font=(fonttype,20, fontstyle), bg='black',fg=foreground)
Title.pack(side=BOTTOM,expand=0)
Title.config(text = 'Project by Group 1: \nDominic Critchlow, Travis Hodge, Dylan Kellogg, Michael Timbes')

# POTUS Twitter
PotusTweet = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground,justify = 'left')
PotusTweet.pack(expand = 0)

# Calendar Label
CalenderLabel = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground)
CalenderLabel.pack(expand = 0)

# Gmail Label
GmailLabel = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground)
GmailLabel.pack(expand = 0)

# Weather Image
WeatherImage = Label(root,bg = 'black')
WeatherImage.pack(expand = 0)
###################################################


###################################################
# Call Function for items
clockUpdate()
weatherAPICall()
stockAPICall()
twitterAPICall()
calendarAPICall()
gmailAPICall()

###################################################




###################################################
# Main structure of window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", exit)
root.configure(background='black')
# Running of the GUI Loop
root.mainloop(  )
###################################################



# Image include with resizing
#image = Image.open("picture.png")
#image = image.resize((250, 250), Image.ANTIALIAS)
#photo = ImageTk.PhotoImage(image)
#label = Label(image=photo)
#label.image = photo # keep a reference!
#label.pack()