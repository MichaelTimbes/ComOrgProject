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
StockTicker = "AAPL"

# size of the weather icon needs to be adjusted for final screen
sizex = 250
sizey = 250
update_speed = 5000

init_run = 0

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
    #time2 = time2 + '\n'+str(today.strftime("%A \n%d %B %Y"))

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
    parameters = {'symbol':StockTicker, 'callback':"jsoncallback"}
    stock = requests.get(url1, params=parameters)
    if stock.status_code == 200:
        stock_json = xmltodict.parse(stock.content)
    print (stock_json)
    StockData.config(text = "Stocks:\n" + stock_json[u'StockQuote'][u'Name']
                            +" $" + stock_json[u'StockQuote'][u'LastPrice'])

    print (stock_json[u'StockQuote'][u'Change'])
    if(float(stock_json[u'StockQuote'][u'Change']) > 0):
        arrow = Image.open("weatherImages/green_arrow.png")
    else:
        arrow = Image.open("weatherImages/red_arrow.png")


    arrow = arrow.resize((75, 85), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(arrow)
    StockImage.configure(image=photo)
    StockImage.image = photo

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
                        + '\n'
                        + str(data[u'main'][u'temp'])
                        + t + 'C')

    WeatherTemp.after(100000,weatherAPICall)

def twitterAPICall():
    consumer_key= '5Sgpga1fHgZ9IxAC5oKMXdHod'
    consumer_secret= 'fU4DN8njObtDCFnr6gYMo03e40O53iJQ2VDdzOP89zuMabJfFJ'
    access_token='3783517036-bA3q6lemHcLgu9QFOX0FJMoqUYR1UPLlaNKQO0g'
    access_token_secret='CEguhLq6UtHzUw304tzjM4iO3WhgkmUfDyAeMhEn19Xhn'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    potus_tweet = api.user_timeline(screen_name = 'cnnbrk',count=3)
    result_tweet = "-> " + potus_tweet[0].text + "\n \n-> " + potus_tweet[1].text + "\n\n-> " + potus_tweet[2].text
    print(result_tweet)
    result_tweet = re.sub(r"(?:\@|https?\://)\S+", "", result_tweet)

    print (result_tweet)
    PotusTweet.config(text = result_tweet)

    PotusTweet.after(update_speed, twitterAPICall)

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
    calendertext = ''
    if not events:
        print('No Upcoming Events Found!')
        CalenderLabel.config(text = 'No Upcoming Events Found!')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            calendertext += event['start'].get('dateTime', event['start'].get('date'))+ " " + event['summary'] + "\n"
            CalenderLabel.config(text = calendertext)

    CalenderLabel.after(update_speed, calendarAPICall)

def gmailAPICall():

    global init_run
    global gmail_unread_messages
    credentials = get_credentials_gmail()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results1 = service.users().messages().list(userId = 'me', q = 'is:unread',maxResults = 5).execute()
    unread_mes_num = results1.get(u'resultSizeEstimate')
    unread_mes_id = results1.get(u'messages',[])
    print ("number of message: " + str(unread_mes_num) + '\n ')
    print (unread_mes_id)


    popUpMessage = ''
    if init_run == 1:
        if gmail_unread_messages < unread_mes_num:
            mess = service.users().messages().get(userId='me', id=unread_mes_id[0][u'id'], format='metadata').execute()
            print(mess)
            mess = mess[u'payload']
            for header in mess[u'headers']:
                if header[u'name'] == u'Subject':
                    popUpMessage = header[u'value']
                    break

            GmailPopUp_Lable(popUpMessage)


    gmail_unread_messages = unread_mes_num
    subject = [None]*10
    i=0
    if unread_mes_num == 0:
        print("No Unread Messages!")
        GmailLabel.config(text="No Unread Messages!")

    else:
        for unreads in unread_mes_id:
            message1 = service.users().messages().get(userId='me', id=unreads[u'id'], format='metadata').execute()
            msg = message1[u'payload']
            print(msg)

            for header in msg[u'headers']:
                if header[u'name'] == u'Subject':
                    subject[i] = header[u'value']
                    break
            if subject:
                print (subject)
            i += 1
        GmailLabel.config(text=(subject[0] + "\n"))


    init_run = 1
    GmailLabel.after(update_speed, gmailAPICall)

def displayWeatherImage(description):

    # Add other weather conditions here you see come through the description until we find a complete list

    if(description == 'sunny'):
        image = Image.open("weatherImages/sunny.png")
    elif(description == 'cloudy'):
        image = Image.open("weatherImages/cloudy.png")
    elif (description == 'rainy'):
        image = Image.open("weatherImages/rainy.png")
    elif (description == 'thunder'):
        image = Image.open("weatherImages/thunder.png")
    elif (description == 'scattered clouds'):
        image = Image.open("weatherImages/scattered clouds.png")
    elif (description == 'overcast clouds'):
        image = Image.open("weatherImages/cloudy.png")
    elif (description == 'clear sky'):
        image = Image.open("weatherImages/sunny.png")
    else:
        image = Image.open("weatherImages/scattered clouds.png")


    image = image.resize((sizex, sizey), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    WeatherImage.configure(image=photo)
    WeatherImage.image = photo

def GmailPopUp_Lable(gmail_text):

    GmailPopUp_Title.config(text = "Gmail Alert \nUnread Message")
    GmailPopUp.config(text = gmail_text)
    GmailPopUp.after(10000,GmailPopUp_Label_destroy)

def GmailPopUp_Label_destroy():

    GmailPopUp_Title.config(text = "")
    GmailPopUp.config(text ="")
###################################################



###################################################
# Initializing root. Main GUI Object Window
root = Tk()
###################################################


###################################################################

# Clock Object ####################################################
#clock_logo = Image.open("weatherImages/clock_logo.png")
#clock_logo = clock_logo.resize((45, 45), Image.ANTIALIAS)
#photo_clock = ImageTk.PhotoImage(clock_logo)
#Clock_Disp = Label(root, font=(fonttype,25,fontstyle),bg='black',fg= foreground,justify = 'left',
                    #image =photo_clock,text = 'Current Time',compound = 'left' )

#Clock_Disp.pack(expand =0)

time1 = ''
Clock = Label(root, font=(fonttype, 30, fontstyle), bg='black',fg=foreground)

Clock.place(x=1010, y=20)

Date = Label(root, font=(fonttype, 20, fontstyle), bg='black',fg=foreground)

Date.config (text = str(datetime.date.today().strftime("%A %d %B %Y")))

Date.place(x=480, y=100)
###################################################################


# Weather Object ##################################################

WeatherImage = Label(root,bg = 'black')
WeatherImage.place(x=1000, y=70)

WeatherTemp = Label(root, font=(fonttype,20,fontstyle),bg='black',fg= foreground, wraplength = 250)
WeatherTemp.place(x=1010, y=270)

###################################################################


# Stock Object ####################################################
StockData = Label(root, font=(fonttype,20,fontstyle),bg='black',fg= foreground,justify = 'left')
StockData.place(x=1000, y=450)

StockImage = Label(root,bg = 'black')
StockImage.place(x=900, y=450)
###################################################################


# Greeting Object #################################################
DayGreet = Label(root, font=(fonttype, 50, fontstyle), bg='black',fg=foreground)
DayGreet.place(x=300, y=10)
###################################################################


# Footer ##########################################################
Footer = Label(root, font=(fonttype,15, fontstyle), bg='black',fg=foreground)
Footer.config(text = 'Project by Group 1: \nDominic Critchlow, Travis Hodge, Dylan Kellogg, Michael Timbes')
Footer.place(x=200, y=950)
###################################################################


# Twitter #########################################################
twitter_logo = Image.open("weatherImages/twitter_logo.png")
twitter_logo = twitter_logo.resize((45, 45), Image.ANTIALIAS)
photo_twitter = ImageTk.PhotoImage(twitter_logo)
TwitterNews = Label(root, font=(fonttype,25,fontstyle),bg='black',fg= foreground,justify = 'left',
                    image =photo_twitter,text = 'Twitter News',compound = 'left' )
TwitterNews.place(x=10, y= 200)
PotusTweet = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground,justify = 'left',wraplength=300, anchor=NW)
PotusTweet.place(x =10, y=250)
###################################################################


# Calendar Label ##################################################
calendar_logo = Image.open("weatherImages/calendar_logo.png")
calendar_logo = calendar_logo.resize((30, 30), Image.ANTIALIAS)
photo_calendar = ImageTk.PhotoImage(calendar_logo)
Calendar_Note = Label(root, font=(fonttype,25,fontstyle),bg='black',fg= foreground,justify = 'left',
                    image =photo_calendar,text = 'Calendar',compound = 'left',wraplength=500, anchor=NW )
Calendar_Note.place(x = 10 ,y = 550)

CalenderLabel = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground)
CalenderLabel.place(x= 10, y=600)
###################################################################


# Gmail Label #####################################################
gmail_unread_messages = ''
gmail_logo = Image.open("weatherImages/mail_logo.png")
gmail_logo = gmail_logo.resize((35, 35), Image.ANTIALIAS)
photo_mail = ImageTk.PhotoImage(gmail_logo)
gmail_Note = Label(root, font=(fonttype,25,fontstyle),bg='black',fg= foreground,justify = 'left',
                    image =photo_mail,text = 'Mail',compound = 'left' , anchor=NW)
gmail_Note.place(x=10,y=700)

GmailLabel = Label(root, font=(fonttype,12,fontstyle),bg='black',fg= foreground,wraplength=300, justify = 'left')
GmailLabel.place(x=10,y=750)

GmailPopUp_Title= Label(root,font=(fonttype,20,fontstyle),bg='red',fg= 'black',justify = 'left')
GmailPopUp_Title.pack()
GmailPopUp_Title.place(x=20,y=20)
GmailPopUp = Label(root,font=(fonttype,12,fontstyle),bg='red',fg= 'black',wraplength=200,justify = 'left')
GmailPopUp.place(x=20,y=100)

###################################################################





###################################################################
# Call Function for items
clockUpdate()
weatherAPICall()
stockAPICall()
twitterAPICall()
calendarAPICall()
gmailAPICall()
#GmailPopUp_Lable("hello")

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
